'use client'
import InfoBlock from '../components/InfoBlock.tsx';
import {RecipeItem} from "../types";
import { useState, useEffect } from 'react';
import axios from 'axios';

function toTitleCase(str: string): string {
    return str.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function Nutrition() {
    const [querySearch, setQuerySearch] = useState('');
    const [searchedRecipes, setSearchedRecipes] = useState<{ query: string }[]>([]);
    const [recipes, setRecipes] = useState<RecipeItem[]>([]);
    const [searchedRecipe, setSearchedRecipe] = useState<RecipeItem | null>(null);
    const [recommendedRecipes, setRecommendedRecipes] = useState<RecipeItem[]>([]);

    useEffect(() => {
        axios.get('/api/v1/recipes/10')
            .then(res => {
                console.log('Response data:', res.data);
                setRecipes(res.data);
            })
            .catch(err => {
                console.log(err);
            });
    }, []);

    const recipeComponents = (
        <div className="wrapper">
            {recipes.map((recipe, index) => (
                <div key={index} className={`item item${index + 1}`}>
                    <InfoBlock
                        title={recipe.name}
                        heading={<h2 className="text-gray-800 text-2xl text-center font-orbital font-bold">{recipe.name}</h2>}
                        text={[
                            recipe.duration ? <div>Duration: {recipe.duration}</div> : "",
                            recipe.rating ? <div>Rating: {recipe.rating}</div> : "",
                        ]}
                        recipe={recipe}
                        fadeInAnimation="fadeIn"
                        bg="bg-[#3E92CC]" // bg-info equivalent
                        url={recipe.url}
                        expandable={true}
                    />
                </div>
            ))}
        </div>
    );

    async function getQuery(query: string) {
        if (query === '') {
            setQuerySearch('');
            setSearchedRecipes([]);
            return;
        }
        setQuerySearch(query);
        try {
            const promise = await axios.post(`/api/v1/recipes/${query.toLowerCase()}`);
            setSearchedRecipes(promise.data);
        } catch {
            setSearchedRecipes([]);
        }
    }

    useEffect(() => {
        getQuery(querySearch);
    }, [querySearch]);

    return (
        <>
            <div className='heroback py-5 w-full mx-auto' id='nutrition-header'>
                <div className="h-16"></div>
                <h1 className='text-primary font-orbital font-bold text-4xl py-5 my-5 text-center'>Search for Personalized Recipes shipped right to your door</h1>

                <h3 className="text-primary text-3xl font-orbital font-bold text-center">Search for recipes from our personalized catalogue</h3>

                {recipeComponents}

                <div className='bg-info w-1/4 min-w-[500px] mx-auto' style={{
                    border: '1rem solid rgba(0, 255, 255, .5)',
                    boxShadow: '8px 8px 3px rgba(0, 255, 125, 1)',
                    padding: '20px',
                    borderRadius: '2px'
                }}>
                    <h2 className='text-primary text-3xl font-orbital font-bold py-8 text-center'>Recommend recipes</h2>
                    {searchedRecipe !== null ? (
                        <InfoBlock
                            bg='bg-[#faebd7] w-1/3' // bg-primary equivalent
                            title={searchedRecipe.name}
                            heading={<h1 className="text-gray-800 text-2xl font-orbital font-bold text-center">{searchedRecipe.name}</h1>}
                            recipe={searchedRecipe}
                            text={[]}
                            expandable={true}
                        />
                    ) : null}

                    <div className='flex justify-center rounded-md'>
                        <div className='w-1/2 flex justify-between'>
                            <button
                                className="w-1/2 text-lg border border-primary text-primary hover:bg-primary hover:text-black my-2 mx-1 py-2 px-4 rounded-md transition-all"
                                type="submit"
                                id='recipeSearch'
                                onClick={() => {
                                    console.log("Query"+querySearch)
                                    console.log("Searched Recipe"+searchedRecipe?.name)
                                    axios.get(`/api/v1/recipes/recipe/${encodeURIComponent(querySearch)}`).then((res) => {
                                        console.log(res.data);
                                        setSearchedRecipe(res.data);
                                        axios.get(`api/v1/recipes/recommendations?query=${encodeURIComponent(querySearch)}&ingredients=${res.data?.ingredients}`).then(async (res) => {
                                            console.log(res.data);
                                            const data: RecipeItem[] = []
                                            for (const name of res.data) {
                                                console.log(name)
                                                await axios.get(`/api/v1/recipes/recipe/${encodeURIComponent(name)}`).then((res) => {
                                                    console.log(res.data)
                                                    if (res.data) data.push(res.data);
                                                })
                                            }
                                            console.log(data)
                                            setRecommendedRecipes(data);
                                        });
                                    });
                                }}>
                                Search
                            </button>
                            <button
                                className="w-1/2 text-lg border border-primary text-primary hover:bg-primary hover:text-black my-2 mx-1 py-2 px-4 rounded-md transition-all"
                                type="submit"
                                id='clear'
                                onClick={() => {
                                    setRecommendedRecipes([]);
                                    setQuerySearch('');
                                    setSearchedRecipe(null);
                                }}>
                                Clear
                            </button>
                        </div>
                    </div>

                    <div className='flex justify-center'>
                        <div className='w-1/2 mb-3'>
                            <input
                                className="w-full p-2 border-4  border-[#00A76E] bg-amber-50 rounded focus:outline-none focus:ring focus:ring-[#C62368] focus:border-[#C62368]" // border-danger equivalent
                                id='navSearch'
                                type="search"
                                placeholder="Search"
                                value={querySearch}
                                onChange={(e) => setQuerySearch(e.target.value)}
                                aria-label="Search"
                            />
                        </div>
                    </div>
                </div>

                {searchedRecipes.length > 0 && (
                    <div className='flex justify-center'>
                        <div className='w-1/2'>
                            <ul className={`bg-white border-primary rounded-lg border border-gray-200 divide-y divide-gray-200`}>
                                {searchedRecipes.map((val, ind) => (
                                    <li
                                        onMouseOut={(ele) => {
                                            const target = ele.target as HTMLElement;
                                            target.classList.remove('bg-gray-100')
                                        }}
                                        onMouseEnter={(ele) => {
                                            const target = ele.target as HTMLElement;
                                            target.classList.add('bg-gray-100')
                                        }}
                                        onClick={(ele) => {
                                            const target = ele.target as HTMLElement;
                                            setQuerySearch(target.innerText)
                                        }}
                                        className='px-4 py-2 cursor-pointer'
                                        key={ind}>
                                        {toTitleCase(val.query)}
                                    </li>))}
                            </ul>
                        </div>
                    </div>
                )}
                {recommendedRecipes.length !== 0 && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5 justify-center">
                        {recommendedRecipes.map((recipe, index) => (
                            <div key={index} className="flex justify-center">
                                <InfoBlock
                                    title={recipe.name}
                                    heading={<h2 className="text-gray-800 text-2xl font-orbital font-bold text-center">{recipe.name}</h2>}
                                    text={[
                                        recipe.duration ? <div>Duration: {recipe.duration}</div> : "",
                                        recipe.rating ? <div>Rating: {recipe.rating}</div> : "",
                                    ]}
                                    recipe={recipe}
                                    icon={recipe.imgSrc}
                                    fadeInAnimation="fadeIn"
                                    bg="bg-info" // bg-info equivalent
                                    url={recipe.url}
                                    expandable={true}
                                />
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </>
    );
}

export default Nutrition;