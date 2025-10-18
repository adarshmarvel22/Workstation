// Responsive JavaScript for Workstation Hub
// Add this to your main.js or create responsive.js

// ===== MOBILE MENU =====
document.addEventListener('DOMContentLoaded', function() {
    // Create mobile menu if it doesn't exist
    if (window.innerWidth <= 968 && !document.querySelector('.mobile-menu')) {
        createMobileMenu();
    }

    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            handleResponsiveLayout();
        }, 250);
    });

    // Initial setup
    handleResponsiveLayout();
});

function createMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;

    // Create mobile menu button
    const mobileBtn = document.createElement('button');
    mobileBtn.className = 'mobile-menu-btn';
    mobileBtn.innerHTML = '<i class="fas fa-bars"></i>';
    mobileBtn.setAttribute('aria-label', 'Toggle menu');

    // Insert mobile button
    const navLeft = document.querySelector('.nav-left');
    if (navLeft) {
        navLeft.appendChild(mobileBtn);
    }

    // Create mobile menu overlay
    const mobileMenu = document.createElement('div');
    mobileMenu.className = 'mobile-menu';
    mobileMenu.innerHTML = `
        <div class="mobile-menu-links">
            ${navLinks.innerHTML}
        </div>
    `;
    document.body.appendChild(mobileMenu);

    // Toggle menu
    mobileBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        mobileMenu.classList.toggle('active');
        const icon = mobileBtn.querySelector('i');
        icon.className = mobileMenu.classList.contains('active') ?
            'fas fa-times' : 'fas fa-bars';
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!mobileMenu.contains(e.target) && !mobileBtn.contains(e.target)) {
            mobileMenu.classList.remove('active');
            mobileBtn.querySelector('i').className = 'fas fa-bars';
        }
    });

    // Close menu when clicking a link
    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
            mobileMenu.classList.remove('active');
            mobileBtn.querySelector('i').className = 'fas fa-bars';
        });
    });
}

// ===== MOBILE FILTERS (EXPLORE PAGE) =====
function initMobileFilters() {
    const sidebar = document.querySelector('.sidebar-left');
    if (!sidebar || window.innerWidth > 1200) return;

    // Create filter button if it doesn't exist
    if (!document.querySelector('.mobile-filter-btn')) {
        const filterBtn = document.createElement('button');
        filterBtn.className = 'mobile-filter-btn btn btn-outline';
        filterBtn.innerHTML = '<i class="fas fa-filter"></i> Filters';

        const mainArea = document.querySelector('.main-area');
        if (mainArea) {
            mainArea.insertBefore(filterBtn, mainArea.firstChild);
        }

        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-mobile-overlay';
        document.body.appendChild(overlay);

        // Make sidebar slideable
        sidebar.classList.add('mobile-active');

        // Toggle filters
        filterBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            overlay.classList.toggle('active');
        });

        overlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            overlay.classList.remove('active');
        });
    }
}

// ===== MOBILE MESSAGES =====
function initMobileMessages() {
    const messagesWrapper = document.querySelector('.messages-wrapper');
    if (!messagesWrapper || window.innerWidth > 968) return;

    // Add back button to messages header
    const messagesHeader = document.querySelector('.messages-header');
    if (messagesHeader && !messagesHeader.querySelector('.back-btn-mobile')) {
        const backBtn = document.createElement('button');
        backBtn.className = 'back-btn-mobile icon-btn';
        backBtn.innerHTML = '<i class="fas fa-arrow-left"></i>';
        backBtn.setAttribute('aria-label', 'Back to conversations');

        const headerInfo = messagesHeader.querySelector('.header-user-info');
        if (headerInfo) {
            messagesHeader.insertBefore(backBtn, headerInfo);
        }

        backBtn.addEventListener('click', function() {
            messagesWrapper.classList.remove('conversation-active');
        });
    }

    // Handle conversation click
    const conversationItems = document.querySelectorAll('.conversation-item');
    conversationItems.forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth <= 968) {
                messagesWrapper.classList.add('conversation-active');
            }
        });
    });
}

// ===== MOBILE SIDEBAR TOGGLE =====
function initSidebarToggle() {
    if (window.innerWidth > 1200) return;

    const sidebarRight = document.querySelector('.sidebar-right');
    if (!sidebarRight) return;

    // Create toggle button
    if (!document.querySelector('.sidebar-toggle')) {
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'sidebar-toggle';
        toggleBtn.innerHTML = '<i class="fas fa-info-circle"></i>';
        toggleBtn.setAttribute('aria-label', 'Toggle sidebar');
        document.body.appendChild(toggleBtn);

        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-mobile-overlay';
        document.body.appendChild(overlay);

        // Make sidebar slideable
        sidebarRight.classList.add('mobile-active');

        toggleBtn.addEventListener('click', function() {
            sidebarRight.classList.toggle('show');
            overlay.classList.toggle('active');
            const icon = toggleBtn.querySelector('i');
            icon.className = sidebarRight.classList.contains('show') ?
                'fas fa-times' : 'fas fa-info-circle';
        });

        overlay.addEventListener('click', function() {
            sidebarRight.classList.remove('show');
            overlay.classList.remove('active');
            toggleBtn.querySelector('i').className = 'fas fa-info-circle';
        });
    }
}

// ===== RESPONSIVE LAYOUT HANDLER =====
function handleResponsiveLayout() {
    const width = window.innerWidth;

    // Initialize mobile features based on screen size
    if (width <= 968) {
        initMobileMessages();
    }

    if (width <= 1200) {
        initMobileFilters();
        initSidebarToggle();
    }

    // Handle search visibility
    const searchBox = document.querySelector('.search-box');
    if (searchBox) {
        if (width <= 640) {
            searchBox.style.display = 'none';
            // Create mobile search button if needed
            createMobileSearch();
        } else {
            searchBox.style.display = 'flex';
        }
    }
}

// ===== MOBILE SEARCH =====
function createMobileSearch() {
    if (document.querySelector('.mobile-search-btn')) return;

    const navRight = document.querySelector('.nav-right');
    if (!navRight) return;

    const searchBtn = document.createElement('button');
    searchBtn.className = 'mobile-search-btn icon-btn';
    searchBtn.innerHTML = '<i class="fas fa-search"></i>';
    searchBtn.setAttribute('aria-label', 'Search');

    // Insert before first child
    navRight.insertBefore(searchBtn, navRight.firstChild);

    // Create mobile search overlay
    const searchOverlay = document.createElement('div');
    searchOverlay.className = 'mobile-search-overlay';
    searchOverlay.innerHTML = `
        <div class="mobile-search-container">
            <button class="mobile-search-close">
                <i class="fas fa-times"></i>
            </button>
            <div class="mobile-search-input">
                <i class="fas fa-search"></i>
                <input type="text" placeholder="Search projects, ideas, people..." id="mobileSearchInput">
            </div>
        </div>
    `;
    document.body.appendChild(searchOverlay);

    // Toggle search
    searchBtn.addEventListener('click', function() {
        searchOverlay.classList.add('active');
        document.getElementById('mobileSearchInput').focus();
    });

    searchOverlay.querySelector('.mobile-search-close').addEventListener('click', function() {
        searchOverlay.classList.remove('active');
    });

    // Handle search
    document.getElementById('mobileSearchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch(this.value);
            searchOverlay.classList.remove('active');
        }
    });
}

// ===== TOUCH GESTURES =====
let touchStartX = 0;
let touchStartY = 0;
let touchEndX = 0;
let touchEndY = 0;

document.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
}, false);

document.addEventListener('touchend', function(e) {
    touchEndX = e.changedTouches[0].screenX;
    touchEndY = e.changedTouches[0].screenY;
    handleSwipe();
}, false);

function handleSwipe() {
    const diffX = touchEndX - touchStartX;
    const diffY = touchEndY - touchStartY;
    const threshold = 50;

    // Horizontal swipe
    if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > threshold) {
        if (diffX > 0) {
            // Swipe right - close sidebars
            closeMobileSidebars();
        } else {
            // Swipe left - could open sidebar
        }
    }
}

function closeMobileSidebars() {
    const sidebar = document.querySelector('.sidebar-left.show, .sidebar-right.show');
    const overlay = document.querySelector('.sidebar-mobile-overlay.active');
    const mobileMenu = document.querySelector('.mobile-menu.active');

    if (sidebar) {
        sidebar.classList.remove('show');
    }
    if (overlay) {
        overlay.classList.remove('active');
    }
    if (mobileMenu) {
        mobileMenu.classList.remove('active');
    }
}

// ===== VIEWPORT HEIGHT FIX FOR MOBILE BROWSERS =====
function setVH() {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

window.addEventListener('resize', setVH);
window.addEventListener('orientationchange', setVH);
setVH();

// ===== SCROLL TO TOP BUTTON (MOBILE) =====
function initScrollToTop() {
    if (window.innerWidth > 768) return;

    if (!document.querySelector('.scroll-to-top')) {
        const scrollBtn = document.createElement('button');
        scrollBtn.className = 'scroll-to-top';
        scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        scrollBtn.setAttribute('aria-label', 'Scroll to top');
        scrollBtn.style.display = 'none';
        document.body.appendChild(scrollBtn);

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollBtn.style.display = 'flex';
            } else {
                scrollBtn.style.display = 'none';
            }
        });

        scrollBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Initialize scroll to top
initScrollToTop();

// ===== LAZY LOADING IMAGES =====
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== PULL TO REFRESH (MOBILE) =====
let startY = 0;
let isPulling = false;

if ('ontouchstart' in window && window.innerWidth <= 768) {
    document.addEventListener('touchstart', function(e) {
        if (window.pageYOffset === 0) {
            startY = e.touches[0].pageY;
            isPulling = true;
        }
    });

    document.addEventListener('touchmove', function(e) {
        if (isPulling) {
            const currentY = e.touches[0].pageY;
            const pullDistance = currentY - startY;

            if (pullDistance > 80) {
                // Show refresh indicator
                showPullToRefreshIndicator();
            }
        }
    });

    document.addEventListener('touchend', function(e) {
        if (isPulling) {
            const currentY = e.changedTouches[0].pageY;
            const pullDistance = currentY - startY;

            if (pullDistance > 80) {
                // Refresh page
                location.reload();
            }

            isPulling = false;
            hidePullToRefreshIndicator();
        }
    });
}

function showPullToRefreshIndicator() {
    if (!document.querySelector('.pull-refresh-indicator')) {
        const indicator = document.createElement('div');
        indicator.className = 'pull-refresh-indicator';
        indicator.innerHTML = '<i class="fas fa-sync fa-spin"></i>';
        document.body.insertBefore(indicator, document.body.firstChild);
    }
}

function hidePullToRefreshIndicator() {
    const indicator = document.querySelector('.pull-refresh-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// ===== RESPONSIVE TABLES =====
function makeTablesResponsive() {
    const tables = document.querySelectorAll('table');

    tables.forEach(table => {
        if (!table.parentElement.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
}

makeTablesResponsive();

// ===== MOBILE FORM IMPROVEMENTS =====
function improveMobileForms() {
    if (window.innerWidth > 768) return;

    // Auto-scroll to input on focus
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            setTimeout(() => {
                this.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }, 300);
        });
    });

    // Add done button for number inputs
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.setAttribute('inputmode', 'numeric');
    });
}

improveMobileForms();

// ===== ORIENTATION CHANGE HANDLER =====
window.addEventListener('orientationchange', function() {
    // Close all mobile menus and overlays
    closeMobileSidebars();

    // Recalculate layout
    setTimeout(() => {
        handleResponsiveLayout();
        setVH();
    }, 300);
});

// ===== RESPONSIVE IMAGE GALLERY =====
function initResponsiveGallery() {
    const galleryImages = document.querySelectorAll('.gallery-image');

    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                openImageModal(this.src);
            }
        });
    });
}

function openImageModal(src) {
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <div class="image-modal-content">
            <button class="image-modal-close">
                <i class="fas fa-times"></i>
            </button>
            <img src="${src}" alt="Full size">
        </div>
    `;
    document.body.appendChild(modal);

    modal.addEventListener('click', function(e) {
        if (e.target === modal || e.target.closest('.image-modal-close')) {
            modal.remove();
        }
    });

    // Pinch to zoom
    let scale = 1;
    const imgElement = modal.querySelector('img');

    imgElement.addEventListener('touchstart', function(e) {
        if (e.touches.length === 2) {
            e.preventDefault();
        }
    });
}

// ===== MOBILE STICKY HEADER =====
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

if (navbar && window.innerWidth <= 768) {
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }

        lastScrollTop = scrollTop;
    }, false);
}

// ===== MOBILE CARD ACTIONS =====
function initMobileCardActions() {
    if (window.innerWidth > 768) return;

    const projectCards = document.querySelectorAll('.project-card');

    projectCards.forEach(card => {
        let touchStartTime;

        card.addEventListener('touchstart', function() {
            touchStartTime = Date.now();
        });

        card.addEventListener('touchend', function(e) {
            const touchDuration = Date.now() - touchStartTime;

            // Long press (500ms) shows action menu
            if (touchDuration > 500) {
                e.preventDefault();
                showCardActionMenu(this);
            }
        });
    });
}

function showCardActionMenu(card) {
    const menu = document.createElement('div');
    menu.className = 'mobile-action-menu';
    menu.innerHTML = `
        <div class="mobile-action-menu-content">
            <button class="action-menu-item">
                <i class="fas fa-heart"></i> Support
            </button>
            <button class="action-menu-item">
                <i class="fas fa-user-plus"></i> Join
            </button>
            <button class="action-menu-item">
                <i class="fas fa-share"></i> Share
            </button>
            <button class="action-menu-item">
                <i class="fas fa-bookmark"></i> Save
            </button>
            <button class="action-menu-close">Cancel</button>
        </div>
    `;
    document.body.appendChild(menu);

    setTimeout(() => menu.classList.add('active'), 10);

    menu.querySelector('.action-menu-close').addEventListener('click', function() {
        menu.classList.remove('active');
        setTimeout(() => menu.remove(), 300);
    });
}

initMobileCardActions();

// ===== BOTTOM SHEET COMPONENT =====
function createBottomSheet(title, content) {
    const sheet = document.createElement('div');
    sheet.className = 'bottom-sheet';
    sheet.innerHTML = `
        <div class="bottom-sheet-overlay"></div>
        <div class="bottom-sheet-content">
            <div class="bottom-sheet-handle"></div>
            <div class="bottom-sheet-header">
                <h3>${title}</h3>
                <button class="bottom-sheet-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="bottom-sheet-body">
                ${content}
            </div>
        </div>
    `;
    document.body.appendChild(sheet);

    setTimeout(() => sheet.classList.add('active'), 10);

    // Close handlers
    const closeSheet = () => {
        sheet.classList.remove('active');
        setTimeout(() => sheet.remove(), 300);
    };

    sheet.querySelector('.bottom-sheet-overlay').addEventListener('click', closeSheet);
    sheet.querySelector('.bottom-sheet-close').addEventListener('click', closeSheet);

    // Swipe down to close
    let sheetStartY = 0;
    const sheetContent = sheet.querySelector('.bottom-sheet-content');

    sheetContent.addEventListener('touchstart', function(e) {
        sheetStartY = e.touches[0].pageY;
    });

    sheetContent.addEventListener('touchmove', function(e) {
        const currentY = e.touches[0].pageY;
        const diff = currentY - sheetStartY;

        if (diff > 0) {
            sheetContent.style.transform = `translateY(${diff}px)`;
        }
    });

    sheetContent.addEventListener('touchend', function(e) {
        const currentY = e.changedTouches[0].pageY;
        const diff = currentY - sheetStartY;

        if (diff > 100) {
            closeSheet();
        } else {
            sheetContent.style.transform = 'translateY(0)';
        }
    });

    return sheet;
}

// ===== MOBILE TOAST IMPROVEMENTS =====
function showMobileToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `mobile-toast mobile-toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ===== HAPTIC FEEDBACK (for supported devices) =====
function triggerHaptic(type = 'light') {
    if ('vibrate' in navigator) {
        switch(type) {
            case 'light':
                navigator.vibrate(10);
                break;
            case 'medium':
                navigator.vibrate(20);
                break;
            case 'heavy':
                navigator.vibrate(50);
                break;
        }
    }
}

// Add haptic to buttons
document.querySelectorAll('.btn, .icon-btn').forEach(btn => {
    btn.addEventListener('click', () => triggerHaptic('light'));
});

// ===== NETWORK STATUS INDICATOR =====
function initNetworkStatus() {
    window.addEventListener('online', function() {
        showMobileToast('Back online', 'success');
    });

    window.addEventListener('offline', function() {
        showMobileToast('No internet connection', 'error');
    });
}

initNetworkStatus();

// ===== MOBILE PERFORMANCE OPTIMIZATIONS =====

// Debounce scroll events
let scrollTimeout;
window.addEventListener('scroll', function() {
    if (scrollTimeout) {
        window.cancelAnimationFrame(scrollTimeout);
    }

    scrollTimeout = window.requestAnimationFrame(function() {
        // Handle scroll events here
    });
});

// Throttle resize events
let resizeTimeout;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function() {
        handleResponsiveLayout();
    }, 250);
});

// ===== EXPORT FUNCTIONS FOR GLOBAL USE =====
window.responsiveUtils = {
    createBottomSheet,
    showMobileToast,
    triggerHaptic,
    closeMobileSidebars,
    handleResponsiveLayout
};

console.log('Responsive JavaScript loaded successfully ✓');