document.addEventListener('DOMContentLoaded', () => {
    const blogGridWrapper = document.querySelector('.blog-grid-wrapper');

    if (!blogGridWrapper) return; 

    const DEFAULT_IMAGE = "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80";

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

            blogGridWrapper.innerHTML = ''; 

            // Mostrar apenas os 3 posts mais recentes no grid da home
            const recentPosts = posts.slice(0, 3);

            recentPosts.forEach(post => {
                const imageUrl = post.image.startsWith('http') ? post.image : post.image;
                const postUrl = post.url;

                const postCard = `
                    <div class="blog-post-card">
                        <div class="blog-post-card-inner">
                            <div class="blog-post-image-container" id="grid-img-container-${post.slug}" style="background: #eee; height: 200px; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                                <img 
                                    src="${imageUrl}" 
                                    alt="${post.title}" 
                                    style="width: 100%; height: 100%; object-fit: cover; display: block;"
                                    onerror="this.onerror=null; this.src='${DEFAULT_IMAGE}';"
                                >
                            </div>
                            <div class="blog-post-content">
                                <h3>${post.title}</h3>
                                <p>${post.excerpt}</p>
                                <a href="${postUrl}" class="read-more">Leia Mais <i class="fas fa-arrow-right"></i></a>
                            </div>
                        </div>
                    </div>
                `;
                blogGridWrapper.innerHTML += postCard;
            });

        } catch (error) {
            console.error('Erro ao carregar posts do blog:', error);
            blogGridWrapper.innerHTML = '<p>Não foi possível carregar as publicações do blog no momento.</p>';
        }
    };

    loadBlogPosts();
});
