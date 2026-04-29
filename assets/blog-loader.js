document.addEventListener('DOMContentLoaded', () => {
    const blogMagazineContainer = document.querySelector('.blog-magazine-container');

    if (!blogMagazineContainer) return; 

    const DEFAULT_IMAGE = "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80";

    const getBaseUrl = () => {
        return '/';
    };

    const loadBlogPosts = async () => {
        try {
            const baseUrl = getBaseUrl();
            let response = await fetch(`${baseUrl}blog/posts/index.json`);
            
            // Fallback caso o baseUrl falhe
            if (!response.ok) {
                response = await fetch('blog/posts/index.json');
            }
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const posts = await response.json();

            blogMagazineContainer.innerHTML = ''; 

            // Selecionar 3 posts de categorias diferentes
            const selectedPosts = [];
            const usedCategories = new Set();

            for (const post of posts) {
                const category = post.categories && post.categories.length > 0 ? post.categories[0] : 'Geral';
                if (!usedCategories.has(category)) {
                    selectedPosts.push(post);
                    usedCategories.add(category);
                }
                if (selectedPosts.length === 3) break;
            }

            // Se não houver 3 categorias diferentes, preencher com os mais recentes que faltam
            if (selectedPosts.length < 3) {
                for (const post of posts) {
                    if (!selectedPosts.find(p => p.slug === post.slug)) {
                        selectedPosts.push(post);
                    }
                    if (selectedPosts.length === 3) break;
                }
            }

            if (selectedPosts.length > 0) {
                const featured = selectedPosts[0];
                const sidePosts = selectedPosts.slice(1);

                let featuredTitle = featured.title;
                if (featured.title.includes(':')) {
                    const parts = featured.title.split(':');
                    featuredTitle = `<span class="gold-highlight">${parts[0]}</span>:${parts.slice(1).join(':')}`;
                }

                let html = `
                    <div class="blog-featured-post">
                        <div class="magazine-card featured" onclick="window.location.href='${featured.url}'">
                            <div class="magazine-image">
                                <img src="${featured.image}" alt="${featured.title}" onerror="this.onerror=null; this.src='${DEFAULT_IMAGE}';">
                            </div>
                            <div class="magazine-content">
                                <h3>${featuredTitle}</h3>
                                <p>${featured.excerpt}</p>
                            </div>
                        </div>
                    </div>
                <div class="blog-side-posts">
                `;

                sidePosts.forEach(post => {
                    // Lógica para destacar a primeira parte do título antes de ":"
                    let displayTitle = post.title;
                    if (post.title.includes(':')) {
                        const parts = post.title.split(':');
                        displayTitle = `<span class="gold-highlight">${parts[0]}</span>:${parts.slice(1).join(':')}`;
                    }

                    html += `
                        <div class="magazine-card compact" onclick="window.location.href='${post.url}'">
                            <div class="magazine-image">
                                <img src="${post.image}" alt="${post.title}" onerror="this.onerror=null; this.src='${DEFAULT_IMAGE}';">
                            </div>
                            <div class="magazine-content">
                                <h3>${displayTitle}</h3>
                                <p class="mobile-hide">${post.excerpt}</p>
                            </div>
                        </div>
                    `;
                });

                html += `</div>`;
                blogMagazineContainer.innerHTML = html;
            }

        } catch (error) {
            console.error('Erro ao carregar posts do blog:', error);
            blogMagazineContainer.innerHTML = '<p>Não foi possível carregar as publicações do blog no momento.</p>';
        }
    };

    loadBlogPosts();
});
