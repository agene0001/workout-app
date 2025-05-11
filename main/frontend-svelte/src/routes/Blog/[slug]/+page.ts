// workout-app/main/frontend-svelte/src/routes/blog/[slug]/+page.server.js

import axios from 'axios';

export const load = async ({ params }) => {
	const slug = params.slug;

	try {
		const res = await axios.get(`/api/v1/blog/posts/slug/${slug}`);
		// console.log(res.data[0])
		// Assuming the structure: data in `res.data`
		return {  post: res.data[0]  };
	} catch (error) {
		console.error('Failed to fetch the blog post:', error);

		return {
			status: error.response ? error.response.status : 500,
			error: new Error('Failed to fetch the blog post.')
		};
	}
};
