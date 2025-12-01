export function createPageUrl(pageName) {
    if (pageName === 'Inicio') return '/';
    return `/${pageName.toLowerCase()}`;
}
