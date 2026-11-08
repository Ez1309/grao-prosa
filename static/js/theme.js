/**
 * Grão & Prosa - Alternância de Tema Claro / Escuro
 * Utiliza o atributo 'data-bs-theme' do Bootstrap 5.3 e persistência em 'localStorage'
 */

(function () {
    const root = document.documentElement;
    const btn = document.getElementById("themeToggle");

    // Aplica o tema no elemento <html> e atualiza o botão
    function applyTheme(theme) {
        root.setAttribute("data-bs-theme", theme);
        try {
            localStorage.setItem("theme", theme);
        } catch (e) {
            console.warn("localStorage indisponível:", e);
        }

        if (btn) {
            if (theme === "dark") {
                btn.innerHTML = 'Tema <i class="fa-solid fa-sun text-warning ms-1" aria-hidden="true"></i>';
                btn.setAttribute("aria-label", "Alternar para tema claro");
            } else {
                btn.innerHTML = 'Tema <i class="fa-solid fa-moon icon-coffee ms-1" aria-hidden="true"></i>';
                btn.setAttribute("aria-label", "Alternar para tema escuro");
            }
        }
    }

    // Identifica o tema salvo ou fallback para light
    function getSavedTheme() {
        try {
            const saved = localStorage.getItem("theme");
            if (saved === "dark" || saved === "light") {
                return saved;
            }
        } catch (e) {}

        if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
            return "dark";
        }
        return "light";
    }

    // Inicialização
    const initialTheme = getSavedTheme();
    applyTheme(initialTheme);

    // Event listener do clique
    if (btn) {
        btn.addEventListener("click", function () {
            const currentTheme = root.getAttribute("data-bs-theme");
            const newTheme = currentTheme === "light" ? "dark" : "light";
            applyTheme(newTheme);
        });
    }
})();
