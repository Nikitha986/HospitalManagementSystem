document.addEventListener("DOMContentLoaded", () => {
    const html = document.documentElement;
    const saved = localStorage.getItem("theme") || "light";
    html.setAttribute("data-theme", saved);

    window.toggleTheme = () => {
        const current = html.getAttribute("data-theme");
        const next = current === "light" ? "dark" : "light";
        html.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
    };
});
