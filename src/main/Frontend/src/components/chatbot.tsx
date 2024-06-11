import {useState} from "react";

function Chatbot() {
    const [helpStart, setHelpStart] = useState(<></>)
    const [toggleState, setToggleState] = useState(false)
    return (
        <div>
            {helpStart}
            <input type='button' onClick={() => {
                if (toggleState) {
                    setHelpStart(<div className='bg-success'>
                        <ul className='nav nav-pills flex-column'>
                            <li className='nav-item m-4 p-3'><a href='#' className='nav-link'>hi</a></li>
                            <li className='nav-item m-4 p-3'><input type='text'/></li>
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