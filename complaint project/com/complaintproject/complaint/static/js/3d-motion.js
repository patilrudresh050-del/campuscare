(function () {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const scene = document.createElement("div");
    scene.className = "scene-3d";
    scene.setAttribute("aria-hidden", "true");

    const shapes = [
        ["11%", "12%", "90px", "-8px", "-18deg", "7s", "20px"],
        ["82%", "8%", "120px", "12deg", "32deg", "9s", "55px"],
        ["76%", "72%", "68px", "-4px", "18deg", "6s", "15px"],
        ["16%", "76%", "110px", "8px", "48deg", "8s", "40px"],
        ["48%", "6%", "55px", "-2px", "-12deg", "5s", "25px"],
        ["43%", "82%", "78px", "5px", "22deg", "7.5s", "30px"]
    ];

    shapes.forEach(function (shape) {
        const item = document.createElement("span");
        item.style.setProperty("--left", shape[0]);
        item.style.setProperty("--top", shape[1]);
        item.style.setProperty("--size", shape[2]);
        item.style.setProperty("--depth", shape[3]);
        item.style.setProperty("--rotation", shape[4]);
        item.style.setProperty("--speed", shape[5]);
        item.style.setProperty("--depth", shape[6]);
        scene.appendChild(item);
    });
    document.body.prepend(scene);

    if (reduceMotion) return;

    const card = document.querySelector(".container");
    if (!card) return;

    card.classList.add("ambient-3d");
    let pointerInside = false;

    card.addEventListener("mousemove", function (event) {
        pointerInside = true;
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        card.classList.remove("ambient-3d");
        card.style.transform =
            "perspective(1200px) " +
            "rotateY(" + (x * 7).toFixed(2) + "deg) " +
            "rotateX(" + (-y * 7).toFixed(2) + "deg) " +
            "translateZ(8px)";
        scene.style.transform =
            "rotateY(" + (x * 2).toFixed(2) + "deg) " +
            "rotateX(" + (-y * 2).toFixed(2) + "deg)";
    });

    card.addEventListener("mouseleave", function () {
        pointerInside = false;
        card.classList.add("ambient-3d");
        card.style.transform = "perspective(1200px) rotateY(0deg) rotateX(0deg) translateZ(0)";
        scene.style.transform = "rotateY(0deg) rotateX(0deg)";
    });

    window.addEventListener("mousemove", function (event) {
        if (pointerInside) return;
        const x = event.clientX / window.innerWidth - 0.5;
        const y = event.clientY / window.innerHeight - 0.5;
        scene.style.transform =
            "rotateY(" + (x * 3).toFixed(2) + "deg) " +
            "rotateX(" + (-y * 3).toFixed(2) + "deg)";
    });
})();
