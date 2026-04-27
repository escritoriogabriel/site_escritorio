document.addEventListener('DOMContentLoaded', () => {
    const blogCarouselWrapper = document.querySelector('.blog-carousel-wrapper');
    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');

    if (!blogCarouselWrapper) return; // Exit if carousel wrapper not found

    let currentIndex = 0;
    let postsPerPage = 3; // Default for desktop

    const updatePostsPerPage = () => {
        if (window.innerWidth <= 768) {
            postsPerPage = 1;
        } else if (window.innerWidth <= 1024) {
            postsPerPage = 2;
        } else {
            postsPerPage = 3;
        }
    };

    const loadBlogPosts = async () => {
        try {
            const response = await fetch('/site_escritorio/blog/posts/index.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const posts = await response.json();

            blogCarouselWrapper.innerHTML = ''; // Clear existing posts

            posts.forEach(post => {
                const postCard = `
                    <div class="blog-post-card">
                        <div class="blog-post-card-inner">
                            <img src="${post.image}" alt="${post.title}">
                            <div class="blog-post-content">
                                <h3>${post.title}</h3>
                                <p>${post.excerpt}</p>
                                <a href="${post.url}" class="read-more">Leia Mais <i class="fas fa-arrow-right"></i></a>
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
        const maxIndex = Math.ceil(totalPosts / postsPerPage) - 1;

        if (currentIndex < 0) {
            currentIndex = maxIndex;
        } else if (currentIndex > maxIndex) {
            currentIndex = 0;
        }

        const offset = -currentIndex * (100 / postsPerPage);
        blogCarouselWrapper.style.transform = `translateX(${offset}%)`;

        // Hide/show buttons if there are not enough posts to scroll
        if (totalPosts <= postsPerPage) {
            prevButton.style.display = 'none';
            nextButton.style.display = 'none';
        } else {
            prevButton.style.display = 'block';
            nextButton.style.display = 'block';
        }
    };

    prevButton.addEventListener('click', () => {
        currentIndex--;
        updateCarousel();
    });

    nextButton.addEventListener('click', () => {
        currentIndex++;
        updateCarousel();
    });

    window.addEventListener('resize', () => {
        updatePostsPerPage();
        updateCarousel();
    });

    loadBlogPosts();
});
