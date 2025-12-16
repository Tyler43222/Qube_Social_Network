import { createButton, createFileUpload, initFormData, setDisplays, initLikes, getCSRFToken } from './utils.js';

let editingPost = false;

export function initPost(post_div) {
    if (!post_div) return;
    // Navigation
    const linkArea = post_div.classList.contains('post-link') ? post_div : post_div.querySelector('.post-link');
    if (linkArea && !linkArea.dataset.navInit) {
        linkArea.dataset.navInit = '1';
        linkArea.addEventListener('click', function(event) {
            // Don't load page if user clicked on a button, link, input, or is editing post
            if (editingPost || event.target.closest('button, a, input, textarea')) return;
            const url = this.getAttribute('data-url');
            if (url) window.location.href = url;
        });
    }
    // Like feature
    initLikes('post', post_div);

    // Edit feature
    post_div.querySelectorAll('.edit').forEach(edit => {
        if (edit.dataset.editInit) return;                       
        edit.dataset.editInit = '1'; 

        const post_div = edit.closest('.post-style');
        const post_id = post_div.dataset.postId;
        const content = post_div.querySelector('.post-content');
        const image = post_div.querySelector('.post-image');

        // Create buttons and image upload fields
        const edit_button = createButton('Edit');
        const save_button = createButton('Save Changes');
        const delete_button = createButton('Delete Post');
        const upload = createFileUpload(image ? 'Change Image' : 'Add Image');

        const text = document.createElement('textarea');
        text.maxLength = 1200;
        text.rows = 4;
        text.value = content.innerText.trim();
        content.parentNode.insertBefore(text, content.nextSibling);

        text.parentNode.insertBefore(upload.container, text.nextSibling);

        const buttonGroup = document.createElement('div');
        buttonGroup.style.display = 'flex';
        buttonGroup.style.gap = '15px';
        buttonGroup.style.flexWrap = 'wrap';
        buttonGroup.append(save_button, delete_button);
       
        edit.append(edit_button, buttonGroup);
        // Only show edit button initially
        setDisplays({'none': [save_button, text, upload.container, delete_button]});

        edit_button.addEventListener('click', () => {
            editingPost = true;
            setDisplays({'none': [content, edit_button], 'block': [save_button, text, upload.container, delete_button]});
            if (image) image.style.display = 'none';
        });
        delete_button.addEventListener('click', () => {
            if (!confirm('Are you sure you want to delete this post?')) return;
            fetch(`/post/${post_id}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    post_div.remove();
                    editingPost = false;
                    if (window.location.pathname.startsWith("/post/detail/")) {
                        window.location.href = "/";
                    }
                } 
                else {
                    alert(data.error || 'Failed to delete post.');
                }
            });
        });
        save_button.addEventListener('click', () => {
            editingPost = false;
            // Create FormData to handle file upload
            const formData = initFormData('content', text, 'image', upload.input)
            
            // Update post content when save is pressed
            fetch(`/post/${ post_id }/update/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    content.textContent = data.content;
                    content.style.display = 'block';
                    if (data.image_url) {
                        if (image) {
                            image.src = data.image_url;
                            image.style.display = 'block';
                        } 
                        else {
                            // Create new image element if it doesn't exist
                            const new_image = document.createElement('img');
                            new_image.className = 'post-image';
                            new_image.src = data.image_url;
                            new_image.alt = 'Image';
                            content.parentNode.insertBefore(new_image, content.nextSibling);
                        }
                    } 
                    else if (image) {
                        image.style.display = 'none';
                    }
                    upload.filename.innerHTML = '';
                    setDisplays({'none': [save_button, text, upload.container, delete_button], 'block': [edit_button]});
                }
            });
        });
    });
}

export function editProfilePhoto(){
    document.querySelectorAll('.settings').forEach(edit => {
        if (edit.dataset.photoInit) return;
        edit.dataset.photoInit = '1';
        
        const profileImage = document.querySelector('.profile-image');
        const profileBio = document.querySelector('.profile-bio');
        
        // Create buttons and image upload fields
        const edit_button = createButton('Edit Profile');
        const save_button = createButton('Save Changes');
        const delete_button = createButton('Remove Profile Photo');
        delete_button.style.marginBottom = '20px';
        const upload = createFileUpload('Upload Profile Photo');
        upload.container.append(delete_button);

        const bio_input = document.createElement('textarea');
        bio_input.placeholder = 'Add a biography';
        bio_input.maxLength = 300;
        bio_input.rows = 4;
        bio_input.value = profileBio ? profileBio.innerText : '';
        
        edit.append(upload.container, bio_input, edit_button, save_button);
        // Initial visibility
        setDisplays({'none': [save_button, upload.container, bio_input]});
        
        edit_button.addEventListener('click', () => {
            setDisplays({'none': [edit_button], 'block': [save_button, upload.container, bio_input]});
        });
        save_button.addEventListener('click', () => {
            // Update profile photo using form data for file upload
            const formData = initFormData('bio_text', bio_input, 'profile_photo', upload.input)

            fetch(`/profile/update/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.photo_url) {
                        if (profileImage) {
                            profileImage.src = data.photo_url;
                        } 
                        else {
                            // Create new image if doesn't exist
                            const new_image = document.createElement('img');
                            new_image.className = 'profile-image';
                            new_image.src = data.photo_url;
                            new_image.alt = 'Profile Photo';
                            edit.parentNode.insertBefore(new_image, edit);
                        }
                    }
                    profileBio.textContent = bio_input.value;
                    upload.filename.innerHTML = '';
                    setDisplays({'none': [save_button, upload.container, bio_input], 'block': [edit_button]});
                } 
                else {
                    alert(data.error || 'Failed to update');
                }
            });
        });
        delete_button.addEventListener('click', () => {
            if (!confirm('Are you sure you want to remove your profile photo?')) return;
            fetch(`/profile/photo/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (profileImage) {
                        profileImage.src = '/static/default-avatar.png';
                    }
                    upload.input.value = '';
                    upload.filename.innerHTML = '';
                    setDisplays({'none': [save_button, upload.container, bio_input], 'block': [edit_button]});
                }
            });
        });
    });
}