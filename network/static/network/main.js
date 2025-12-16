import { initPost, editProfilePhoto } from './edit.js';
import { initLikes, infiniteScroll } from './utils.js';

document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.posts-container'); 
    if (!container) return;
    const commentsContainer = document.querySelector('.comments-container');
    
    // Category buttons
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active-category'));
            btn.classList.add('active-category');
        });
    });
    
    container.querySelectorAll('.post-style').forEach(initPost);
    initLikes('post', document);
    initLikes('comment', document);
    editProfilePhoto();
    
    // Post image upload preview
    const fileInput = document.getElementById("file-input");
    const fileName = document.querySelector(".file-name");
    if (fileInput && fileName) {
        fileInput.onchange = function() {
            fileName.innerHTML = this.files[0] ? `<img src="${URL.createObjectURL(this.files[0])}">` : "";
        };
    }
    
    // Initialize comment likes for newly loaded comments
    const initCommentLikes = (comment) => {
            initLikes('comment', comment);
    };

    if (commentsContainer) {
        infiniteScroll(commentsContainer, '.comment-style', initCommentLikes);
    }
    infiniteScroll(container, '.post-style', initPost);
});