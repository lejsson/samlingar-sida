"use strict";
let post_box_container = document.getElementById('post-box-container');
if (post_box_container) {
    const sortable = new Sortable.create(post_box_container, {
        handle: '#grid-icon',
        touchStartThreshold: 10,
        filter: ".add-box",
        onMove: function (evt) {
            return evt.related.className.indexOf('add-box') === -1;
        },
        animation: 150
    });
}
//post_box
// Options for the observer (which mutations to observe)
const config = {
    childList: true, // Observe changes to the child nodes
    subtree: false // Don't observe changes in descendant nodes
};
// Callback function to execute when mutations are observed
const callback = (mutationsList) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'childList') {
            console.log('A child node has been added or removed.');
        }
        // You can also check for any specific changes in the order of elements
        // For instance, if you want to log the new order of children:
        const children = Array.from(post_box_container.children);
        console.log('Current order of children:', children.map(child => child.id || child.className));
    }
};
// Create an instance of MutationObserver and pass the callback
const observer = new MutationObserver(callback);
// Start observing the target node for configured mutations
if (post_box_container) {
    observer.observe(post_box_container, config);
}
