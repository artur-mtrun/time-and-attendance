export function formatDateTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleString(); // Możesz dostosować formatowanie według potrzeb
} 