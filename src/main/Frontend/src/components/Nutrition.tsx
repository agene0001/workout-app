'use client'
import InfoBlock from './/InfoBlock'
import React, {useState, useEffect, useRef} from 'react'
import axios from 'axios'
import Granim from 'granim'
import anime, {engine} from 'animejs'

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
    const [buildRecipes, setBuildRecipes] = useState([])
    const recipeRef = useRef();
    const caloriesRef = useRef("");
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

        var duration = 10000
        var ease = 'easeInOutQuint'
        var direction = 'alternate'
        console.log(buildRecipes)
        console.log(recommendedRecipes.length)
    }, [])
    const recipeComponents = recipes.map((item: any[]) => {
        let data = item.filter(val => val != null);
        return (<div className='row'> {data.map((elementLis, idx) => (
            <InfoBlock key={idx} heading={elementLis.name} bg='bg-info' nutrition={elementLis.nutrition}
                       icon={elementLis.imgSrc} text={[
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
            {/*<div  className='heroback'></div>*/}
            <div className='heroback py-5 container-fluid align-content-center'
                 id='nutrition-header'>
                    <div style={{height: '60px'}}>
                    </div>
                    <h1 className='text-primary py-5 my-5 text-center'>Search for
                        Personalized Recipes shipped right to you door</h1>

                    <div className='row justify-content-center '>

                        <h2 className='text-primary py-5 text-center'>Recommend recipes</h2>


                        <div className="col-auto inline-flex">
                            <button className="btn btn-lg btn-outline-primary my-2 my-sm-0" type="submit"
                                    id='recipeSearch' onClick={() => {
                                axios.get(`/recommendations?query=${encodeURIComponent(querySearch)}`).then((res) => {
                                    console.log(res.data)
                                    setRecommendedRecipes(res.data)
                                    // console.log(typeof(res.data))
                                })
                                // setQuerySearch(ele.target.innerHTML)
                            }}>Search
                            </button>
                            <button className="btn btn-lg btn-outline-primary my-2 my-sm-0" type="submit"
                                    id='clear' onClick={() => {
                                setRecommendedRecipes([])
                                // console.log(typeof(res.data))
                            }
                                // setQuerySearch(ele.target.innerHTML)
                            }>Clear
                            </button>
                        </div>
                        <div className='col-7'>
                            <input className="form-control border-danger border-4 mr-sm-2" id='navSearch' type="search"
                                   placeholder="Search" value={querySearch}
                                   onChange={(e) => {
                                       setQuerySearch(e.target.value);
                                       // getQuery(e.target.value)
                                   }
                                   }
                                   aria-label="Search"/>

                            <ul className="list-group" style={{height: '25vh', overflow: 'scroll'}}>
                                {searchedRecipes.map((val, ind) => (<li onMouseOut={(ele) => {
                                    ele.target.classList.remove('active')
                                }} onMouseEnter={(ele) => {
                                    ele.target.classList.add('active')
                                }} onClick={(ele) => {
                                    setQuerySearch(ele.target.innerText)
                                }} className='list-group-item' key={ind}>{toTitleCase(val.query)}</li>))}
                            </ul>
                    </div>
                </div>

                {/*<div className='row'>*/}
                {/*    {Object.values(recommendedRecipes).map((val, index) => <div className='col-6'><InfoBlock key={index}*/}
                {/*                                                                                             heading={val['name']}*/}
                {/*                                                                                             bg='bg-danger'*/}
                {/*                                                                                             text={[val.duration, val.rating]}></InfoBlock>*/}
                {/*    </div>)}*/}
                {/*</div> */}
                {recommendedRecipes.length!==0?
                <div className='wrapper'>
                    {Object.values(recommendedRecipes).map((val, index, arr) => <div className={`item`} style={{
                        animationDelay: `calc(60s / ${arr.length} * (${arr.length} - ${index}) * -1)`,
                        left: `max(calc(300px*${arr.length}), 100%)`
                    }}><InfoBlock key={index} heading={val['name']}
                                  bg='bg-danger' text={[val.duration, val.rating]}></InfoBlock>
                    </div>)}
                </div>:<></>
                }
                {/*<div className='wrapper'>*/}
                {/*    <div className="item item1"></div>*/}
                {/*    <div className="item item2"></div>*/}
                {/*    <div className="item item3"></div>*/}
                {/*    <div className="item item4"></div>*/}
                {/*    <div className="item item5"></div>*/}
                {/*    <div className="item item6"></div>*/}
                {/*    <div className="item item7"></div>*/}
                {/*    <div className="item item8"></div>*/}
                {/*</div>*/}
            </div>
            <div className='container2'>
                <svg id="visual" viewBox="0 0 920 250" xmlns="http://www.w3.org/2000/svg"
                     version="1.1">
                    <rect x="0" y="0" width="920" height="250" fill="#000000"></rect>
                    <path
                        d="M0 137L21.8 137.8C43.7 138.7 87.3 140.3 131.2 147.2C175 154 219 166 262.8 172C306.7 178 350.3 178 394.2 174.7C438 171.3 482 164.7 525.8 161.8C569.7 159 613.3 160 657.2 160.7C701 161.3 745 161.7 788.8 159C832.7 156.3 876.3 150.7 898.2 147.8L920 145L920 0L898.2 0C876.3 0 832.7 0 788.8 0C745 0 701 0 657.2 0C613.3 0 569.7 0 525.8 0C482 0 438 0 394.2 0C350.3 0 306.7 0 262.8 0C219 0 175 0 131.2 0C87.3 0 43.7 0 21.8 0L0 0Z"
                        fill="#753a88" id='pt1'></path>
                    <path
                        d="M0 149L21.8 139.7C43.7 130.3 87.3 111.7 131.2 106.3C175 101 219 109 262.8 111.7C306.7 114.3 350.3 111.7 394.2 109.2C438 106.7 482 104.3 525.8 106.5C569.7 108.7 613.3 115.3 657.2 121C701 126.7 745 131.3 788.8 128.7C832.7 126 876.3 116 898.2 111L920 106L920 0L898.2 0C876.3 0 832.7 0 788.8 0C745 0 701 0 657.2 0C613.3 0 569.7 0 525.8 0C482 0 438 0 394.2 0C350.3 0 306.7 0 262.8 0C219 0 175 0 131.2 0C87.3 0 43.7 0 21.8 0L0 0Z"
                        fill="#903483" id='pt2'></path>
                    <path
                        d="M0 95L21.8 94.8C43.7 94.7 87.3 94.3 131.2 89.7C175 85 219 76 262.8 77.2C306.7 78.3 350.3 89.7 394.2 97C438 104.3 482 107.7 525.8 103.3C569.7 99 613.3 87 657.2 86.5C701 86 745 97 788.8 101.8C832.7 106.7 876.3 105.3 898.2 104.7L920 104L920 0L898.2 0C876.3 0 832.7 0 788.8 0C745 0 701 0 657.2 0C613.3 0 569.7 0 525.8 0C482 0 438 0 394.2 0C350.3 0 306.7 0 262.8 0C219 0 175 0 131.2 0C87.3 0 43.7 0 21.8 0L0 0Z"
                        fill="#a82e7a" id='pt3'></path>
                    <path
                        d="M0 74L21.8 74.7C43.7 75.3 87.3 76.7 131.2 76.3C175 76 219 74 262.8 74.2C306.7 74.3 350.3 76.7 394.2 75.5C438 74.3 482 69.7 525.8 67.3C569.7 65 613.3 65 657.2 62C701 59 745 53 788.8 50.5C832.7 48 876.3 49 898.2 49.5L920 50L920 0L898.2 0C876.3 0 832.7 0 788.8 0C745 0 701 0 657.2 0C613.3 0 569.7 0 525.8 0C482 0 438 0 394.2 0C350.3 0 306.7 0 262.8 0C219 0 175 0 131.2 0C87.3 0 43.7 0 21.8 0L0 0Z"
                        fill="#bc2a6d" id='pt4'></path>
                    <path
                        d="M0 46L21.8 42.8C43.7 39.7 87.3 33.3 131.2 30.5C175 27.7 219 28.3 262.8 28.2C306.7 28 350.3 27 394.2 29C438 31 482 36 525.8 35.2C569.7 34.3 613.3 27.7 657.2 25.7C701 23.7 745 26.3 788.8 29.2C832.7 32 876.3 35 898.2 36.5L920 38L920 0L898.2 0C876.3 0 832.7 0 788.8 0C745 0 701 0 657.2 0C613.3 0 569.7 0 525.8 0C482 0 438 0 394.2 0C350.3 0 306.7 0 262.8 0C219 0 175 0 131.2 0C87.3 0 43.7 0 21.8 0L0 0Z"
                        fill="#cc2b5e" id='pt5'></path>
                </svg>
            </div>
            {/*<div className='spacer waves3'></div>*/}
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
                        <div className='bg-danger rounded-3'>

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

                            <legend className='text-success py-3 text-center'>Build Your own Diet</legend>
                            <label for='calories' className="p-3 inline-flex">Calories</label>
                            <input ref={caloriesRef} name='calories' type="number" className='rounded-2'
                                   placeholder='3000'/>
                            <div className='py-3'>
                                <button className='btn btn-lg btn-outline-success m-4 my-sm-0' onClick={() => {

                                    axios.get(`/build_recipes?calories=${caloriesRef.current.value}`).then((res) => {
                                        console.log(res.data);
                                        setBuildRecipes(res.data)
                                    })
                                }}>Generate Meal Plan
                                </button>
                            </div>
                            {/* breakfast lunch dinner snacks desserts */}
                        </div>
                        <div className='container-fluid'>
                            {buildRecipes.map((val, index, arr) => {
                                if (index % 2 != 0) {
                                    return <div className='row justify-content-center'>
                                        <InfoBlock key={index}
                                                   heading={val[0].name}
                                                   icon={val[0].img_src}
                                                   bg='bg-danger col-4'
                                                   text={[
                                                       val[0]['types'], val[0].calories + ' calories',
                                                       val[0].ratings]}/>
                                        <InfoBlock key={index - 1}
                                                   heading={arr[index - 1][0].name}
                                                   icon={arr[index - 1][0].img_src}
                                                   bg='bg-danger col-4'
                                                   text={[
                                                       arr[index - 1][0]['types'], arr[index - 1][0].calories + ' calories',
                                                       arr[index - 1][0].ratings]}/>
                                    </div>
                                }
                            })

                            }
                        </div>
                    </div>
                </div>
            </div>
            <div className='spacer waves2'></div>
            <div className='lowPoly3 heroback '>
                <button className='btn btn-lg btn-secondary m-4 my-sm-0' onClick={() => {
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
                    })
                }}>
                    Generate Random Recipes
                </button>

                <div className='row' ref={recipeRef} style={{display: 'inline-flex'}}>
                    {recipeComponents}
                </div>
            </div>
        </>
    )
}


export default Nutrition