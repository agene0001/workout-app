'use client'
import InfoBlock from './InfoBlock'; /* Corrected from './/InfoBlock' */
import {useState, useEffect} from 'react';
import axios from 'axios';

function toTitleCase(str: string): string {
    return str.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

interface RecipeItem {
    name: string;
    nutrition: string;
    imgSrc: string;
    duration: string;
    rating: number;
    url: string;
}

function Nutrition() {
    const [querySearch, setQuerySearch] = useState('');
    const [searchedRecipes, setSearchedRecipes] = useState<{ query: string }[]>([]);
    const [recipes, setRecipes] = useState<RecipeItem[][]>([]);
    const [searchedRecipe, setSearchedRecipe] = useState<RecipeItem | null>(null);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [recommendedRecipes, setRecommendedRecipes] = useState<RecipeItem[]>([]);
    // const [buildRecipes, setBuildRecipes] = useState<RecipeItem[]>([]);
    // const recipeRef = useRef<HTMLDivElement>(null);
    // const caloriesRef = useRef<HTMLInputElement>(null);
    useEffect(() => {

    }, [recommendedRecipes]);
    useEffect(() => {
        axios.get('/api/v1/recipes/10')
            .then(res => {
                console.log('Response data:', res.data);
                if (Array.isArray(res.data)) {
                    console.log(res.data);

                    const data = res.data.filter((item: RecipeItem) => item.imgSrc !== null);
                    const arr = [];
                    for (let i = 0; i < data.length; i += 3) {
                        const newArr = [];
                        for (let j = 0; j < 3; j++) {
                            if (data[i + j]) newArr.push(data[i + j]);
                        }
                        arr.push(newArr);
                    }
                    setRecipes(arr);
                } else {
                    console.error('Expected an array but got:', res.data);
                }
            })
            .catch(err => {
                console.log(err);
            });
    }, []);

    const recipeComponents = recipes.map((row, rowIndex) => (
        <div className='row' style={{ display: 'flex' }} key={`row-${rowIndex}`}>
            {row.map((recipe) => (
                <div className="col-4" style={{ display: 'flex', justifyContent: 'center' }} key={recipe.name}>
                    <InfoBlock
                        key={recipe.name}
                        title={recipe.name}
                        heading={<h1>{recipe.name}</h1>}
                        bg='bg-info'
                        nutrition={recipe.nutrition}
                        icon={recipe.imgSrc}
                        text={[
                            recipe.duration?<div>Duration: {recipe.duration}</div>:"",
                            recipe.rating?<div>Rating: {recipe.rating}</div>:"",
                        ]}
                       url={recipe.url}
                     expandable={true} ingredients={""}/>
                </div>
            ))}
        </div>
    ));

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

    return (<>
        <div className='heroback py-5 container-fluid align-content-center' id='nutrition-header'>
            <div style={{height: '60px'}}></div>
            <h1 className='text-primary py-5 my-5'>Search for Personalized Recipes shipped right to your door</h1>
            {recommendedRecipes.length!=0?
                <div className="wrapper">
                    {recommendedRecipes.map((recipe, index) => (
                        <div key={index} className={`item item${index + 1}`}>
                            <InfoBlock
                                title={recipe.name}
                                heading={<h2>{recipe.name}</h2>}
                                text={[
                                    recipe.duration?<div>Duration: {recipe.duration}</div>:"",
                                    recipe.rating?<div>Rating: {recipe.rating}</div>:"",
                                ]}
                                icon={recipe.imgSrc}
                                fadeInAnimation="fadeIn" // Or pass the fadeInAnimation prop as needed
                                bg="bg-info" // Optionally change the background color
                                url={recipe.url}
                                expandable={true}
                            />
                        </div>
                    ))}
                </div>:""
            }
            <div className='bg-secondary' style={{
                display: 'inline-block',
                minWidth: '500px',
                backgroundColor: '#f8f9fa',
                border: '1rem solid rgba(255, 0, 255, 1)',
                boxShadow: '8px 8px 3px rgba(255, 255, 0, 1)',
                padding: '20px',
                borderRadius: '2px'
            }}>
                <h2 className='text-primary py-5 text-center'>Recommend recipes</h2>
                {searchedRecipe !== null ? (<InfoBlock
                    bg='bg-primary col-4'
                    title={searchedRecipe.name}
                    heading={<h1>{searchedRecipe.name}</h1>}
                    text={[]}
                    expandable={true}
                />) : null}

                <div className='row justify-content-center'>
                    <div className='col-6 d-flex justify-content-between'>
                        <button
                            className="btn btn-lg w-50 btn-outline-primary my-2 my-sm-0 mx-1" type="submit"
                            id='recipeSearch'
                            onClick={() => {
                                axios.get(`api/v1/recipes/recommendations?query=${encodeURIComponent(querySearch)}`).then(async (res) => {
                                    console.log(res.data);
                                    const data: RecipeItem[] = []
                                    for (const name of res.data) {
                                        console.log(name)
                                        await axios.get(`/api/v1/recipes/recipe/${encodeURIComponent(name)}`).then((res) => {
                                            console.log(res.data)
                                            if (res.data) data.push(res.data);  // Use JSON.stringify() if it's a plain object
                                            // console.log(res)
                                        })
                                    }
                                    console.log(data)
                                    setRecommendedRecipes(data);
                                });
                                axios.get(`/api/v1/recipes/recipe/${encodeURIComponent(querySearch)}`).then((res) => {
                                    console.log(res.data);
                                    setSearchedRecipe(res.data);
                                    console.log(typeof (res.data));
                                });
                            }}>
                            Search
                        </button>
                        <button
                            className="btn btn-lg btn-outline-primary my-2 my-sm-0 w-50 mx-1"
                            type="submit"
                            id='clear'
                            onClick={() => {
                                setRecommendedRecipes([]);
                                setQuerySearch('');
                            }}>
                            Clear
                        </button>
                    </div>
                </div>
                <div className='row justify-content-center'>
                    <div className='col-6 mb-3'>
                        <input
                            className="form-control border-danger border-4 mr-sm-2"
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

            <div className='row justify-content-center'>
                <div className='col-6'>
                    <ul className="list-group">
                        {searchedRecipes.map((val, ind) => (<li
                            onMouseOut={(ele) => {
                                const target = ele.target as HTMLElement; // Cast target to HTMLElement

                                target.classList.remove('active')
                            }}
                            onMouseEnter={(ele) => {

                                const target = ele.target as HTMLElement; // Cast target to HTMLElement

                                target.classList.add('active')
                            }}
                            onClick={(ele) => {
                                const target = ele.target as HTMLElement; // Cast target to HTMLElement

                                setQuerySearch(target.innerText)
                            }}

                            className='list-group-item'
                            key={ind}>
                            {toTitleCase(val.query)}
                        </li>))}
                    </ul>
                </div>
            </div>
            {recipeComponents}
        </div>
    </>);
}

export default Nutrition;