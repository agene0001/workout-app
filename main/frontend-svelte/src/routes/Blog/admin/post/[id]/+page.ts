import axios from 'axios';
import type { LoadEvent } from '@sveltejs/kit';

export const load = async ({ params }: LoadEvent) => {
    const id = params.id;

    if (id === 'new') {
        // For a new post, return a default structure or an indicator
        return {
            post: {
                title: '',
                content: { blocks: [{ type: 'paragraph', data: { text: 'Start writing your blog post here...' } }] }, // Default empty editor content
                category: '', // Default or ensure categories are loaded for selection
                // Add any other default fields your Post model might expect
            },
            isNew: true
        };
    } else {
        // For an existing post, fetch its data
        try {
            const res = await axios.get(`/api/v1/blog/posts/id/${id}`);
            return {
                post: res.data, // Assuming res.data is the post object
                isNew: false
            };
        } catch (error: any) {
            console.error('Failed to fetch the blog post for editing:', error);
            // SvelteKit expects a specific error structure for error pages
            return {
                status: error.response ? error.response.status : 500,
                error: new Error('Failed to fetch the blog post for editing.')
            };
        }
    }
};
