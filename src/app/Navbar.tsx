"use client"
import React from 'react'
import NavDropdown from 'react-bootstrap/NavDropdown'

import 'bootstrap/dist/js/bootstrap.js'

function Navbar(props: { name: string }) {
    const NavItem = (props: { text: string }) => {
        const [isHovered, setIsHovered] = React.useState(false);
        return (
            <li
                className={`nav-item fs-5 p-3 m-3 ${isHovered ? "customHover" : ""}`}
                onMouseOver={() => setIsHovered(true)}
                onMouseOut={() => setIsHovered(false)}
            >
                {props.text}
            </li>
        );
    }
    const NavDropItem = (props: { text: string }) => {
        const [isHovered, setIsHovered] = React.useState(false);
        return (<NavDropdown.Item href="/"
                                  className={`fs-5 p-3 m-3 text-danger ${isHovered ? "customHover" : ''}`}
                                  onMouseOver={() => setIsHovered(true)}
                                  onMouseOut={() => setIsHovered(false)}>
            {props.text}
        </NavDropdown.Item>)
    }
    const NavDropTitle = (props: { text: string }) => {
        const [isHovered, setIsHovered] = React.useState(false);
        return (<span className={`text-danger fs-5 ${isHovered ? 'customHover' : ''}`}
                      onMouseOver={() => setIsHovered(true)} onMouseOut={() => setIsHovered(false)}>{props.text}</span>)

    }
    return (
        <header>
        <nav className="navbar navbar-expand-lg py-1 vw-100 navbar-dark bg-dark sticky-top">
            <div className="container-fluid ">
                <a className="navbar-brand fs-1 fw-semibold p-2" href="/">Gains Tracker</a>

                <button className="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse justify-content-around" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto align-items-center">
                        <NavItem text={<a className={`nav-link ${props.name.toLowerCase() === 'nutrition' ? " active" : " text-danger"}`} href="/Nutrition">Nutrition</a>}/>
                       <NavItem text={<a className={`nav-link ${props.name.toLowerCase() === 'games' ? " active" : " text-danger"}`} href="/Games">Recent Games</a>}/>

                        <NavDropdown title={<NavDropTitle text='Sports'/>} menuVariant='danger'>
                            <NavDropItem text='Martial Arts'/>
                            <NavDropItem text="Court"/>
                            <NavDropItem text='Field Sports'/>
                            <NavDropdown.Divider/>
                            <NavDropItem text='Others'/>
                        </NavDropdown>

                        <li className="nav-item fs-5 p-2 m-3">
                            <a className="nav-link disabled text-danger" href="#">Disabled</a>
                        </li>
                    </ul>
                    <form className="form-inline my-2 my-lg-0">
                        <div className="input-group">
                            <input className="form-control border-danger border-4 mr-sm-2" id='navSearch' type="search"
                                   placeholder="Search"
                                   aria-label="Search"/>
                            <button className="btn btn-outline-danger my-2 my-sm-0" type="submit">Search
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </nav>
            </header>

    );
}

export default Navbar;