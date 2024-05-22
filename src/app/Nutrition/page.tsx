'use client'
import InfoBlock from '../InfoBlock'
import {useState, useEffect} from 'react'
import axios from 'axios'

function Nutrition() {

    const [recipes, setRecipes] = useState([])
    useEffect(() => {
        axios.get('/api/recipes').then(res => {
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
        return (<div className='row' > {data.map((elementLis, idx) => (
            <InfoBlock key={idx} heading={elementLis.name} icon={elementLis.imgSrc} text={[
                <div>{elementLis.duration}</div>,
                <div>Rating: {elementLis.rating}</div>
            ]}/>))} </div>);
    });

    ;
    return (
        <>
            <div className='lowPoly heroback align-content-center'><h1 className='text-info text-center'>Search for
                Personalized Recipes shipped right to you door</h1></div>
            <div className='spacer waves3'></div>
            <div className="heroback layer2 container-fluid" id="hero3">
                <div className='row' style={{display: 'inline-flex'}}>
                    {recipeComponents}
                </div>
            </div>
            <div className='spacer waves2'></div>
            <div className='lowPoly3 heroback'></div>
        </>
    )
}

export default Nutrition