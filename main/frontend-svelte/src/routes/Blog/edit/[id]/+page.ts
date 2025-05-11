
import axios from 'axios';

export const load = async ({ params }) => {
    const id = params.id;
    console.log("id: "+id);
    try {
        const res = await axios.get(`/api/v1/blog/posts/id/${id}`);
        console.log(res.data)
        // Assuming the structure: data in `res.data`
        return {  post: res.data };
    } catch (error) {
        console.error('Failed to fetch the blog post:', error);

        return {
            status: error.response ? error.response.status : 500,
            error: new Error('Failed to fetch the blog post.')
        };
    }
};
