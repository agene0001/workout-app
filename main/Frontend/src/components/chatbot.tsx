import {useState} from "react";

function Chatbot() {
    const [helpStart, setHelpStart] = useState(<></>)
    const [toggleState, setToggleState] = useState(false)
    return (
        <div className='container-fluid text-center'>
            {helpStart}
            <input type='button' onClick={() => {
                if (toggleState) {
                    setHelpStart(<div className='bg-success chatbotAni rounded-3'>
                        <ul className='nav nav-pills flex-column align-content-center'>
                            {/*<li className='nav-item m-4 p-3'><a href='#' className='nav-link'>hi</a></li>*/}
                            <li className='nav-item m-4 p-3'><p className='text-primary d-inline m-3'>Search recipe</p><input type='text'/></li>
                        </ul>
                    </div>)
                    setToggleState(false)
                } else {
                    setHelpStart(<></>)
                    setToggleState(true)
                }
            }} className='btn btn-secondary btn-lg' value='How May I help You'/>
        </div>
    )
}

export default Chatbot