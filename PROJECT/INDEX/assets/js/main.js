// ========================================
// Svetosila Documentation - Main JavaScript
// ========================================

// Generate Table of Contents from headings
function generateTOC() {
    const content = document.querySelector('.content');
    const sidebar = document.querySelector('.sidebar');
    const sidebarList = document.querySelector('.sidebar ul');
    
    if (!content || !sidebar || !sidebarList) return;
    
    const headings = content.querySelectorAll('h2, h3');
    
    if (headings.length === 0) {
        // Hide sidebar if no headings
        sidebar.style.display = 'none';
        return;
    }
    
    // Clear existing TOC
    sidebarList.innerHTML = '';
    
    headings.forEach((heading, index) => {
        // Add ID to heading if it doesn't have one
        if (!heading.id) {
            heading.id = `section-${index}`;
        }
        
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = `#${heading.id}`;
        a.textContent = heading.textContent;
        
        // Indent h3 more than h2
        if (heading.tagName === 'H3') {
            a.style.paddingLeft = '15px';
            a.style.fontSize = '0.85em';
        }
        
        // Add click handler for manual highlight
        a.addEventListener('click', function(e) {
            // Remove active class from all items
            document.querySelectorAll('.sidebar ul li').forEach(item => {
                item.classList.remove('active');
            });
            
            // Add active class to clicked item
            li.classList.add('active');
            
            // Enable manual highlight mode
            isManualHighlight = true;
            lastScrollPosition = window.scrollY || window.pageYOffset;
        });
        
        li.appendChild(a);
        sidebarList.appendChild(li);
    });
    
    // Highlight current section on scroll
    window.addEventListener('scroll', highlightCurrentSection);
    window.addEventListener('scroll', detectUserScroll);
}

// Variables for manual highlight control
let isManualHighlight = false;
let isProgrammaticScroll = false;
let lastScrollPosition = 0;

// Highlight active section in TOC
function highlightCurrentSection() {
    // Skip auto-highlight if manual highlight is active
    if (isManualHighlight) {
        return;
    }
    
    const sections = document.querySelectorAll('.content h2, .content h3');
    const tocLinks = document.querySelectorAll('.sidebar ul li a');
    
    // Get current scroll position
    const scrollPosition = window.scrollY || window.pageYOffset;
    
    // Calculate reference point
    const offset = 100;
    const referencePoint = scrollPosition + offset;
    
    let currentSection = null;
    
    // Find the section that contains the reference point
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        
        if (sectionTop <= referencePoint) {
            currentSection = section.id;
        }
    });
    
    // Highlight the corresponding TOC link
    tocLinks.forEach(link => {
        const li = link.parentElement;
        if (link.getAttribute('href') === `#${currentSection}`) {
            li.classList.add('active');
        } else {
            li.classList.remove('active');
        }
    });
}

// Detect user scroll (not programmatic)
function detectUserScroll() {
    if (isProgrammaticScroll) {
        return;
    }
    
    const currentScrollPosition = window.scrollY || window.pageYOffset;
    
    if (isManualHighlight && Math.abs(currentScrollPosition - lastScrollPosition) > 3) {
        isManualHighlight = false;
        highlightCurrentSection();
    }
    
    lastScrollPosition = currentScrollPosition;
}

// Smooth scroll to anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').slice(1);
            const target = document.getElementById(targetId);
            
            if (target) {
                isProgrammaticScroll = true;
                
                const offsetTop = target.offsetTop - 80;
                const startPosition = window.scrollY || window.pageYOffset;
                const distance = Math.abs(offsetTop - startPosition);
                const duration = Math.min(distance / 2, 1000);
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                setTimeout(() => {
                    isProgrammaticScroll = false;
                }, duration + 100);
            }
        });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    generateTOC();
    initSmoothScroll();
});

