import InfoBlock from './InfoBlock'
import {useState,useEffect} from 'react'
import axios from 'axios'
function Nutrition(){

    const[recipes,setRecipes] = useState([])
    useEffect(()=>{
        axios.get('http://localhost:5001/api/recipes').then(res=>{
            console.log(res);
            console.log(res.data);
        })
    },[])
    return (
        <>
            <div className='lowPoly heroback align-content-center'><h1 className='text-info text-center'>Search for Personalized Recipes shipped right to you door</h1></div>
            <div className='spacer waves3'></div>
            <div className="heroback layer2">
                 <InfoBlock animation='' heading='Recipe 1' text='This is an info block. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa fugit
                           in iste
                           libero magni molestiae neque quod. Accusantium aspernatur cupiditate delectus deleniti
                           deserunt dicta
                           facere fugit iure nihil officiis, quis quo rem saepe sed sit tempore temporibus unde
                           voluptas
                           voluptatum.' icon={null}/>
            </div>
            <div className='spacer waves2'></div>
            <div className='lowPoly3 heroback'></div>
        </>
    )
}

export default Nutrition