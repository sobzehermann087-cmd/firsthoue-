document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const loaderBar = document.getElementById('loader-bar');

    if(loaderBar) loaderBar.style.width = '100%';
    body.classList.remove('is-loading');
    setTimeout(() => {
        if(loaderBar) loaderBar.style.opacity = '0';
    }, 200);

    const links = document.querySelectorAll('.nav-link-transition');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href && !href.startsWith('#') && !href.startsWith('javascript')) {
                if(loaderBar) {
                    loaderBar.style.opacity = '1';
                    loaderBar.style.width = '40%';
                }
            }
        });
    });

    // --- MOBILE MENU BURGER ---
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const mainNav = document.getElementById('main-nav'); // header-nav-desktop
    const navOverlay = document.getElementById('nav-overlay');
    
    function toggleMenu() {
        if (!mainNav || !navOverlay) return;
        mainNav.classList.toggle('mobile-active');
        navOverlay.classList.toggle('active');
        body.style.overflow = mainNav.classList.contains('mobile-active') ? 'hidden' : '';
        
        const icon = menuToggle.querySelector('i');
        if (mainNav.classList.contains('mobile-active')) {
            icon.classList.replace('fa-bars', 'fa-times');
        } else {
            icon.classList.replace('fa-times', 'fa-bars');
        }
    }

    if (menuToggle && mainNav && navOverlay) {
        menuToggle.addEventListener('click', toggleMenu);
        navOverlay.addEventListener('click', toggleMenu);

        // Fermer le menu lors du clic sur un lien (important pour les ancres ou transitions)
        const navLinks = mainNav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (mainNav.classList.contains('mobile-active')) {
                    toggleMenu();
                }
            });
        });
    }

    // --- FONCTION DE RECHERCHE GLOBALE ---
    window.performGlobalSearch = function() {
        const searchInput = document.getElementById('global-search-input');
        if (!searchInput) return;
        
        const query = searchInput.value.toLowerCase().trim();
        console.log("Recherche globale lancée pour :", query);

        // CAS 1 : PAGE CARTE
        if (typeof window.filterMapHotels === 'function') {
            const mapSearchInput = document.getElementById('map-search');
            if (mapSearchInput) mapSearchInput.value = searchInput.value;
            window.filterMapHotels(searchInput.value);
            return;
        }

        // CAS 2 : ACCUEIL / RÉSERVATION
        const cards = document.querySelectorAll('.hotel-card');
        if (cards.length > 0) {
            cards.forEach(card => {
                const text = card.innerText.toLowerCase();
                const hotel = (card.getAttribute('data-hotel') || "").toLowerCase();
                const region = (card.getAttribute('data-region') || "").toLowerCase();
                const prix = parseInt(card.getAttribute('data-prix')) || 0;

                if (query === "") {
                    card.style.display = "block";
                } else if (!isNaN(query) && query !== "") {
                    card.style.display = (prix <= parseInt(query)) ? "block" : "none";
                } else {
                    if (text.includes(query) || hotel.includes(query) || region.includes(query)) {
                        card.style.display = "block";
                    } else {
                        card.style.display = "none";
                    }
                }
            });
        }
    };

    // Attacher l'événement input pour le live-search
    const globalInput = document.getElementById('global-search-input');
    if (globalInput) {
        globalInput.addEventListener('input', window.performGlobalSearch);
        // Gérer la touche Entrée sans recharger la page
        globalInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                window.performGlobalSearch();
            }
        });
    }
});

// Carousel Logic (Inchangé)
let slideIndex = 1;
const slides = document.getElementsByClassName("carousel-slide");
if (slides.length > 0) {
    showSlides(slideIndex);
    setInterval(() => { plusSlides(1); }, 5000);
}
function plusSlides(n) { showSlides(slideIndex += n); }
function showSlides(n) {
    if (slides.length === 0) return;
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (let i = 0; i < slides.length; i++) { slides[i].style.display = "none"; }
    slides[slideIndex-1].style.display = "block";
}
