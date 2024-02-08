/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})



jQuery(document).ready(function() {
    jQuery('.form-outline .form-control').on('focus input', function() {
        jQuery(this).closest('.form-outline').addClass('active'); // Add the 'active' class to the closest 'p' element
    });

    jQuery('.form-outline .form-control').blur(function() {
        if (jQuery(this).val() === '') {
            jQuery(this).closest('.form-outline').removeClass('active'); // Remove the 'active' class from the closest 'p' element
        }
    });
});

jQuery(window).on("load", function() {
    jQuery('.form-outline .form-control').each(function() {
        if (jQuery(this).val()) {
            jQuery(this).closest('.form-outline').addClass('active');
        }
    });
});
