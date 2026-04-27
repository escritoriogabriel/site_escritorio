document.addEventListener('DOMContentLoaded', () => {
    const blogCarouselWrapper = document.querySelector('.blog-carousel-wrapper');
    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');

    if (!blogCarouselWrapper) return; 

    let currentIndex = 0;
    let postsPerPage = 3; 

    const updatePostsPerPage = () => {
        if (window.innerWidth <= 768) {
            postsPerPage = 1;
        } else if (window.innerWidth <= 1024) {
            postsPerPage = 2;
        } else {
            postsPerPage = 3;
        }
    };

    const getBaseUrl = () => {
        const path = window.location.pathname;
        if (path.includes('/site_escritorio/')) {
            return '/site_escritorio/';
        }
        return '/';
    };

    const loadBlogPosts = async () => {
        try {
            const baseUrl = getBaseUrl();
            const response = await fetch(`${baseUrl}blog/posts/index.json`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const posts = await response.json();

            blogCarouselWrapper.innerHTML = ''; 

            posts.forEach(post => {
                // Ajustar caminhos de imagem e URL para serem relativos à base do site
                const fullImageUrl = post.image.startsWith('http') ? post.image : `${baseUrl}${post.image}`;
                const fullPostUrl = post.url.startsWith('http') ? post.url : `${baseUrl}${post.url}`;
                const defaultImage = "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80";

                const postCard = `
                    <div class="blog-post-card">
                        <div class="blog-post-card-inner">
                            <img src="${fullImageUrl}" alt="${post.title}" onerror="this.src='${defaultImage}'">
                            <div class="blog-post-content">
                                <h3>${post.title}</h3>
                                <p>${post.excerpt}</p>
                                <a href="${fullPostUrl}" class="read-more">Leia Mais <i class="fas fa-arrow-right"></i></a>
                            </div>
                        </div>
                    </div>
                `;
                blogCarouselWrapper.innerHTML += postCard;
            });

            updatePostsPerPage();
            updateCarousel();

        } catch (error) {
            console.error('Erro ao carregar posts do blog:', error);
            blogCarouselWrapper.innerHTML = '<p>Não foi possível carregar as publicações do blog no momento.</p>';
        }
    };

    const updateCarousel = () => {
        const totalPosts = blogCarouselWrapper.children.length;
        if (totalPosts === 0) return;

        const maxIndex = Math.ceil(totalPosts / postsPerPage) - 1;

        if (currentIndex < 0) {
            currentIndex = maxIndex;
        } else if (currentIndex > maxIndex) {
            currentIndex = 0;
        }

        const offset = -currentIndex * (100 / postsPerPage);
        blogCarouselWrapper.style.transform = `translateX(${offset}%)`;

        if (totalPosts <= postsPerPage) {
            if (prevButton) prevButton.style.display = 'none';
            if (nextButton) nextButton.style.display = 'none';
        } else {
            if (prevButton) prevButton.style.display = 'block';
            if (nextButton) nextButton.style.display = 'block';
        }
    };

    if (prevButton) {
        prevButton.addEventListener('click', () => {
            currentIndex--;
            updateCarousel();
        });
    }

    if (nextButton) {
        nextButton.addEventListener('click', () => {
            currentIndex++;
            updateCarousel();
        });
    }

    window.addEventListener('resize', () => {
        updatePostsPerPage();
        updateCarousel();
    });

    loadBlogPosts();
});
