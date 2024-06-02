'use client'
import InfoBlock from './/InfoBlock'
import React, {useState, useEffect, useRef} from 'react'
import axios from 'axios'

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function Nutrition() {
    const [querySearch, setQuerySearch] = useState('')
    const [searchedRecipes, setSearchedRecipes] = useState([])
    const [recipes, setRecipes] = useState([])
    const [recommendedRecipes, setRecommendedRecipes] = useState([])
    const recipeRef = useRef();
    useEffect(() => {
        axios.get('/api/v1/recipes/10').then(res => {
            console.log(res.data)
            let data = res.data.filter(item => item.imgSrc !== null)
            let arr = []
            for (let i = 0; i < data.length; i += 3) {
                let newArr = []
                for (let j = 0; j < 3; j++) newArr.push(data[i + j])
                arr.push(newArr)
            }
            setRecipes(arr)
        }).catch(err => {
            console.log(err)
        })
    }, [])
    const recipeComponents = recipes.map((item: any[]) => {
        let data = item.filter(val => val != null);
        return (<div className='row'> {data.map((elementLis, idx) => (
            <InfoBlock key={idx} heading={elementLis.name} bg='bg-info' icon={elementLis.imgSrc} text={[
                <div>{elementLis.duration}</div>,
                <div>Rating: {elementLis.rating}</div>
            ]}/>))} </div>);
    });


    async function getQuery(query) {
        if (query === '') {

            setQuerySearch('')
            setSearchedRecipes([])
            return
        }
        setQuerySearch(query)
        try {
            let promise = await axios.post(`/api/v1/recipes/${query.toLowerCase()}`)
            setSearchedRecipes(promise.data)
        } catch {
            setSearchedRecipes([])
        }
    }

    useEffect(() => {
        getQuery(querySearch)
    }, [querySearch]);
    // Here you can place your asynchronous logic (like ajax calls)

    // function getFormData(object: {}) {
    //     const formData = new FormData();
    //     formData.append('ingredients', JSON.stringify(object));
    //     return formData;
    // }

    return (
        <>
            <div className='lowPoly heroback py-5 container-fluid align-content-center'>
                <div style={{height: '30px'}}>
                </div>
                <h1 className='text-info py-5 text-center'>Search for
                    Personalized Recipes shipped right to you door</h1>

                <div className='row justify-content-center '>
                    <div className='col-auto'>
                        <h4 className='text-info'>Recommend recipes</h4>
                    </div>
                    <div className="col-auto">
                        <input className="form-control border-danger border-4 mr-sm-2" id='navSearch' type="search"
                               placeholder="Search" value={querySearch}
                               onChange={(e) => {
                                   setQuerySearch(e.target.value);
                                   // getQuery(e.target.value)
                               }
                               }
                               aria-label="Search"/>
                        <ul className="list-group" style={{height: 200, overflow: 'scroll'}}>
                            {searchedRecipes.map((val, ind) => (<li onMouseOut={(ele) => {
                                ele.target.classList.remove('active')
                            }} onMouseEnter={(ele) => {
                                ele.target.classList.add('active')
                            }} onClick={(ele) => {
                                setQuerySearch(ele.target.innerText)
                            }} className='list-group-item' key={ind}>{toTitleCase(val.query)}</li>))}
                        </ul>
                    </div>

                    <div className="col-auto justify-content-center">
                        <button className="btn btn-lg btn-outline-danger my-2 my-sm-0" type="submit"
                                id='recipeSearch' onClick={() => {
                            axios.get(`/recommendations?query=${encodeURIComponent(querySearch)}`).then((res) => {
                                console.log(res.data)
                                setRecommendedRecipes(res.data)
                                // console.log(typeof(res.data))
                            })
                            // setQuerySearch(ele.target.innerHTML)
                        }}>Search
                        </button>

                    </div>
                </div>

                <div className='row'>
                    {Object.values(recommendedRecipes).map((val, index) => <div className='col-6'><InfoBlock key={index}
                                                                                                             heading={val['name']}
                                                                                                             bg='bg-danger'
                                                                                                             text={[val.duration, val.rating]}></InfoBlock>
                    </div>)}
                </div>
            </div>
            <div className='spacer waves3'></div>
            <div className="heroback layer2 container-fluid">

                <div className='row justify-content-center'>
                    <div className='col-auto'>
                        {/*<ul className="nav nav-pills bg-info rounded-3">*/}
                        {/*    <li className="nav-item">*/}
                        {/*        <a className="nav-link active" aria-current="page" href="#">Breakfast</a>*/}
                        {/*    </li>*/}
                        {/*    <li className="nav-item">*/}
                        {/*        <a className="nav-link" href="#">Lunch</a>*/}
                        {/*    </li>*/}
                        {/*    <li className="nav-item">*/}
                        {/*        <a className="nav-link" href="#">Easy Main Dish</a>*/}
                        {/*    </li>*/}
                        {/*    <li className="nav-item">*/}
                        {/*        <a className="nav-link" href="#">Hamburgers</a>*/}
                        {/*    </li>*/}
                        {/*    <li className="nav-item">*/}
                        {/*        <a className="nav-link" href="#">Healthy</a>*/}
                        {/*    </li>*/}
                        {/*    <li className="nav-item">*/}
                        {/*        <a className="nav-link" href="#">Desserts</a>*/}
                        {/*    </li>*/}
                        {/*    <li className="nav-item">*/}
                        {/*        <a className="nav-link disabled" href="#" tabIndex="-1"*/}
                        {/*           aria-disabled="true">Disabled</a>*/}
                        {/*    </li>*/}
                        {/*</ul>*/}
                        <form className='bg-danger rounded-3'>

                            <ul className="nav nav-pills bg-secondary rounded-3">
                                <li className="nav-item">
                                    <a className="nav-link active" aria-current="page" href="#">Anything</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="#">Vegan</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="#">Paleo</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="#">Pescatarian</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="#">Vegetarian</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="#">Ketogenic</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="#">Atkins</a>
                                </li>
                            </ul>

                            <legend className=''>Build Your own Diet</legend>
                            <label for='calories' className="p-3">Calories</label>
                            <input id='calories' type="number" className='rounded-2' placeholder='3000'/>
                        {/*
                        breakfast lunch dinner snacks desserts */}
                        </form>
                    </div>
                </div>
            </div>
            <div className='spacer waves2'></div>
            <div className='lowPoly3 heroback'>
                <div className='row' ref={recipeRef} style={{display: 'inline-flex'}}>
                    {recipeComponents}
                </div>
            </div>
        </>
    )
}


export default Nutrition