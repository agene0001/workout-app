

function Navbar() {
    return (
            <nav className="navbar navbar-expand-lg py-1 bg-dark sticky-top">
                <a className="navbar-brand fs-1 fw-semibold p-2" href="#">Gainz Tracker</a>

                <button className="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse justify-content-around" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item fs-5 p-2 m-3 active">
                            <a className="nav-link active" href="#">Home</a>
                        </li>
                        <li className="nav-item  fs-5 p-2 m-3">
                            <a className="nav-link text-danger" href="#">Link</a>
                        </li>
                        <li className="nav-item dropdown fs-5 p-2 m-3">
                            <a className="nav-link dropdown-toggle text-danger" href="#" id="navbarDropdown" role="button"
                               data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Dropdown
                            </a>
                            <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                <a className="dropdown-item" href="#">Action</a>
                                <a className="dropdown-item" href="#">Another action</a>
                                <div className="dropdown-divider"></div>
                                <a className="dropdown-item" href="#">Something else here</a>
                            </div>
                        </li>
                        <li className="nav-item fs-5 p-2 m-3">
                            <a className="nav-link disabled text-danger" href="#">Disabled</a>
                        </li>
                    </ul>
                    <form className="form-inline my-2 my-lg-0">
                        <div className="input-group">
                            <input className= "form-control border-danger border-4 mr-sm-2" id='navSearch' type="search" placeholder="Search"
                                   aria-label="Search"/>
                            <button className="btn btn-outline-danger my-2 my-sm-0" type="submit">Search
                            </button>
                        </div>
                    </form>
                </div>
            </nav>

    );
}

export default Navbar;