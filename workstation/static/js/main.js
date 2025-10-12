// Global functions and utilities

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Toast notification system
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icon = type === 'success' ? 'check-circle' :
                 type === 'error' ? 'exclamation-circle' :
                 'info-circle';

    toast.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(400px)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// User menu dropdown
document.addEventListener('DOMContentLoaded', function() {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');

    if (userMenuBtn && userDropdown) {
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }

    // Notification button
    const notificationBtn = document.getElementById('notificationBtn');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function() {
            window.location.href = '/notifications/';
        });
    }

    // Tab switching
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            const tabName = this.getAttribute('data-tab');
            loadTabContent(tabName);
        });
    });

    // Global search
    const searchInput = document.getElementById('globalSearch');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 500);
        });
    }

    // Filter checkboxes
    const filterCheckboxes = document.querySelectorAll('.checkbox-label input[type="checkbox"]');
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            applyFilters();
        });
    });

    // Filter buttons
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from siblings
            this.parentElement.querySelectorAll('.filter-btn').forEach(b => {
                b.classList.remove('active');
            });
            this.classList.add('active');
            applyFilters();
        });
    });
});

// Load tab content
function loadTabContent(tabName) {
    const gridContainer = document.getElementById('projectsGrid');
    if (!gridContainer) return;

    // Show loading state
    gridContainer.innerHTML = '<div class="loading">Loading...</div>';

    // Fetch content based on tab
    let endpoint = '/api/projects/';
    if (tabName === 'ideas') {
        endpoint += '?project_type=idea';
    } else if (tabName === 'people') {
        endpoint = '/api/users/';
    }

    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            if (tabName === 'people') {
                renderPeople(data.results || data);
            } else {
                renderProjects(data.results || data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            gridContainer.innerHTML = '<div class="error">Failed to load content</div>';
        });
}

// Render projects
function renderProjects(projects) {
    const gridContainer = document.getElementById('projectsGrid');
    if (!gridContainer) return;

    if (projects.length === 0) {
        gridContainer.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <h3>No projects found</h3>
                <p>Try adjusting your filters or search criteria</p>
            </div>
        `;
        return;
    }

    gridContainer.innerHTML = projects.map(project => `
        <div class="project-card">
            <div class="project-image">
                ${project.cover_image ?
                    `<img src="${project.cover_image}" alt="${project.title}">` :
                    `<div class="project-placeholder"><i class="fas fa-code"></i></div>`
                }
                <button class="bookmark-btn" onclick="bookmarkProject('${project.slug}')">
                    <i class="far fa-bookmark"></i>
                </button>
            </div>
            <div class="project-content">
                <h3 class="project-title">
                    <a href="/projects/${project.slug}/">${project.title}</a>
                </h3>
                <p class="project-description">${project.short_description || project.description.substring(0, 100) + '...'}</p>
                <div class="project-tags">
                    ${(project.tags || []).slice(0, 3).map(tag =>
                        `<span class="tag">${tag.name}</span>`
                    ).join('')}
                </div>
                <div class="project-footer">
                    <div class="project-avatars">
                        ${renderAvatars(project.creator)}
                    </div>
                    <div class="project-actions">
                        <button class="action-btn" onclick="joinProject('${project.slug}')">
                            <i class="fas fa-user-plus"></i> Join
                        </button>
                        <button class="action-btn" onclick="supportProject('${project.slug}')">
                            <i class="fas fa-heart"></i> Support
                        </button>
                        <button class="action-btn">
                            <i class="fas fa-comment"></i> Chat
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Render people
function renderPeople(users) {
    const gridContainer = document.getElementById('projectsGrid');
    if (!gridContainer) return;

    gridContainer.innerHTML = users.map(user => `
        <div class="project-card">
            <div class="project-content" style="padding-top: 2rem;">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <div style="width: 80px; height: 80px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 2px solid var(--border-color);">
                        ${user.profile_image ?
                            `<img src="${user.profile_image}" alt="${user.username}" style="width: 100%; height: 100%; object-fit: cover;">` :
                            `<div class="avatar-placeholder-large">${user.username.charAt(0).toUpperCase()}</div>`
                        }
                    </div>
                </div>
                <h3 class="project-title" style="text-align: center;">
                    <a href="/users/${user.username}/">${user.first_name || user.username} ${user.last_name || ''}</a>
                </h3>
                <p class="project-description" style="text-align: center;">${user.title || user.bio || 'Member'}</p>
                <div class="project-tags" style="justify-content: center;">
                    <span class="tag">${user.user_type}</span>
                </div>
                <div class="project-footer" style="justify-content: center; border-top: none;">
                    <button class="btn btn-outline btn-full" onclick="location.href='/messages/send/${user.username}/'">
                        <i class="fas fa-envelope"></i> Message
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Render avatars
function renderAvatars(creator) {
    if (!creator) return '';

    return `
        <div class="avatar-small">
            ${creator.profile_image ?
                `<img src="${creator.profile_image}" alt="${creator.username}">` :
                `<div class="avatar-placeholder-small">${creator.username.charAt(0).toUpperCase()}</div>`
            }
        </div>
    `;
}

// Apply filters
function applyFilters() {
    const selectedStages = Array.from(document.querySelectorAll('input[name="stage"]:checked'))
        .map(cb => cb.value);
    const selectedCollaboration = Array.from(document.querySelectorAll('input[name="collaboration"]:checked'))
        .map(cb => cb.value);
    const selectedStatus = Array.from(document.querySelectorAll('input[name="status"]:checked'))
        .map(cb => cb.value);

    // Build query string
    const params = new URLSearchParams();

    if (selectedStages.length) {
        selectedStages.forEach(stage => params.append('stage', stage));
    }
    if (selectedCollaboration.length) {
        selectedCollaboration.forEach(collab => params.append('collaboration', collab));
    }
    if (selectedStatus.length) {
        selectedStatus.forEach(status => params.append('status', status));
    }

    // Update URL and reload
    window.location.href = `?${params.toString()}`;
}

// Perform search
function performSearch(query) {
    if (!query || query.length < 2) return;

    const params = new URLSearchParams(window.location.search);
    params.set('search', query);
    window.location.href = `?${params.toString()}`;
}

// Support project
function supportProject(slug) {
    fetch(`/projects/${slug}/support/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.supported ? 'Project supported!' : 'Support removed', 'success');
        } else {
            showToast('Failed to support project', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred', 'error');
    });
}

// Join project
function joinProject(slug) {
    // Redirect to project detail page where they can formally join
    window.location.href = `/projects/${slug}/`;
}

// Bookmark project
function bookmarkProject(slug) {
    // Add bookmark functionality
    fetch(`/api/projects/${slug}/support/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const btn = event.currentTarget;
        const icon = btn.querySelector('i');

        if (data.supported) {
            icon.classList.remove('far');
            icon.classList.add('fas');
            showToast('Added to bookmarks', 'success');
        } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
            showToast('Removed from bookmarks', 'info');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Please login to bookmark projects', 'error');
    });
}

// Load more functionality (infinite scroll)
let isLoading = false;
let currentPage = 1;

function setupInfiniteScroll() {
    window.addEventListener('scroll', () => {
        if (isLoading) return;

        const scrollHeight = document.documentElement.scrollHeight;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const clientHeight = window.innerHeight;

        if (scrollTop + clientHeight >= scrollHeight - 500) {
            loadMoreProjects();
        }
    });
}

function loadMoreProjects() {
    isLoading = true;
    currentPage++;

    const params = new URLSearchParams(window.location.search);
    params.set('page', currentPage);

    fetch(`/api/projects/?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.results && data.results.length > 0) {
                appendProjects(data.results);
            }
            isLoading = false;
        })
        .catch(error => {
            console.error('Error:', error);
            isLoading = false;
        });
}

function appendProjects(projects) {
    const gridContainer = document.getElementById('projectsGrid');
    if (!gridContainer) return;

    projects.forEach(project => {
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';
        projectCard.innerHTML = `
            <div class="project-image">
                ${project.cover_image ?
                    `<img src="${project.cover_image}" alt="${project.title}">` :
                    `<div class="project-placeholder"><i class="fas fa-code"></i></div>`
                }
                <button class="bookmark-btn" onclick="bookmarkProject('${project.slug}')">
                    <i class="far fa-bookmark"></i>
                </button>
            </div>
            <div class="project-content">
                <h3 class="project-title">
                    <a href="/projects/${project.slug}/">${project.title}</a>
                </h3>
                <p class="project-description">${project.short_description || project.description.substring(0, 100) + '...'}</p>
                <div class="project-tags">
                    ${(project.tags || []).slice(0, 3).map(tag =>
                        `<span class="tag">${tag.name}</span>`
                    ).join('')}
                </div>
                <div class="project-footer">
                    <div class="project-avatars">
                        ${renderAvatars(project.creator)}
                    </div>
                    <div class="project-actions">
                        <button class="action-btn" onclick="joinProject('${project.slug}')">
                            <i class="fas fa-user-plus"></i> Join
                        </button>
                        <button class="action-btn" onclick="supportProject('${project.slug}')">
                            <i class="fas fa-heart"></i> Support
                        </button>
                        <button class="action-btn">
                            <i class="fas fa-comment"></i> Chat
                        </button>
                    </div>
                </div>
            </div>
        `;
        gridContainer.appendChild(projectCard);
    });
}

// Initialize infinite scroll if on explore page
if (document.getElementById('projectsGrid')) {
    setupInfiniteScroll();
}

// Real-time notifications (optional - would need WebSocket)
function checkNotifications() {
    fetch('/api/notifications/unread_count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.notification-badge');
            if (badge && data.unread_count > 0) {
                badge.textContent = data.unread_count;
                badge.style.display = 'block';
            } else if (badge) {
                badge.style.display = 'none';
            }
        })
        .catch(error => console.error('Error checking notifications:', error));
}

// Check notifications every 30 seconds if user is logged in
if (document.querySelector('.notification-badge')) {
    checkNotifications();
    setInterval(checkNotifications, 30000);
}

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });

    return isValid;
}

// Image preview for file uploads
function setupImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');

    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById(input.id + '_preview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

// Initialize image previews
document.addEventListener('DOMContentLoaded', setupImagePreview);

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('globalSearch');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // Escape to close dropdowns
    if (e.key === 'Escape') {
        const dropdowns = document.querySelectorAll('.dropdown-menu.show');
        dropdowns.forEach(dropdown => dropdown.classList.remove('show'));
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy', 'error');
    });
}

// Debounce helper function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle helper function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
