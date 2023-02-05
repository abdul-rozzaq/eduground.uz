const normalizePozition = (mouseX, mouseY, contextMenu, scope) => {
    let {
        left: scopeOffsetX,
        top: scopeOffsetY,
    } = scope.getBoundingClientRect();

    scopeOffsetX = scopeOffsetX < 0 ? 0 : scopeOffsetX;
    scopeOffsetY = scopeOffsetY < 0 ? 0 : scopeOffsetY;

    const scopeX = mouseX - scopeOffsetX;
    const scopeY = mouseY - scopeOffsetY;

    const outOfBoundsOnX = scopeX 
     + contextMenu.clientWidth > scope.clientWidth;

    const outOfBoundsOnY = scopeY + contextMenu.clientHeight 
    // > scope.clientHeight;

    let normalizedX = mouseX;
    let normalizedY = mouseY;

    // ? normalize on X
    if (outOfBoundsOnX) {
        normalizedX =
            scopeOffsetX + scope.clientWidth - contextMenu.clientWidth;
    }

    // ? normalize on Y
    if (outOfBoundsOnY) {
        normalizedY =
            scopeOffsetY + scope.clientHeight - contextMenu.clientHeight;
    }

    return {
        normalizedX,
        normalizedY
    };
};

const lids = document.getElementsByClassName("lid")
const contextMenu = document.querySelector('#context-menu')
const body = document.querySelector('body')

for (let lid of lids) {

    // lid.addEventListener("contextmenu", (event) => {
    //     event.preventDefault();

    //     const {
    //         clientX: mouseX,
    //         clientY: mouseY
    //     } = event;

    //     const {
    //         normalizedX,
    //         normalizedY
    //     } = normalizePozition(mouseX, mouseY, contextMenu, lid);

    //     contextMenu.classList.remove("visible");

    //     contextMenu.style.top = `${normalizedY}px`;
    //     contextMenu.style.left = `${normalizedX}px`;

    //     setTimeout(() => {
    //         contextMenu.classList.add("visible");
    //     });
    // });

    lid.addEventListener('contextmenu', (event) => {
        event.preventDefault()
    
        const { clientX : mouseX, clientY : mouseY } = event
        
        let windowHeight = window.innerHeight,
            windowWidth = window.innerWidth,
            contextX = mouseX,
            contextY = mouseY 

        if (mouseX > windowWidth - contextMenu.clientWidth){
            contextX = windowWidth - contextMenu.clientWidth
        }

        if (mouseY > windowHeight - contextMenu.clientHeight){
            contextY = windowHeight - contextMenu.clientHeight - 20 
        }

        contextMenu.style.top = `${contextY+10}px`
        contextMenu.style.left = `${contextX}px`
    
        contextMenu.classList.add('visible')
    })  

    lid.addEventListener("click", (e) => {
        if (e.target.offsetParent != contextMenu) {
            contextMenu.classList.remove("visible");
        }
    });
}

body.addEventListener("click", (e) => {
    if (e.target.offsetParent != contextMenu) {
        contextMenu.classList.remove("visible");
    }
});

document.addEventListener("scroll", (e) => {
    if (e.target.offsetParent != contextMenu) {
        contextMenu.classList.remove("visible");
    }
});