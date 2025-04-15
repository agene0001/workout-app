"use client";
import React, {useState} from "react";
import {NavItemProps} from "../types";

function Navbar(props: { name: string }) {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const NavItem: React.FC<NavItemProps> = ({text}) => {
        const [isHovered, setIsHovered] = useState(false);

        return (
            <li
                className={`text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ${isHovered ? "text-secondary scale-105" : "text-[#00dd87]"}`}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
            >
                {text}
            </li>
        );
    };

    return (
        <header className="relative px-4">
            <nav className="bg-zinc-900 text-danger sticky top-0 shadow-md rounded-2xl py-4">
                <div className="container mx-auto px-4">
                    <div className="flex items-center justify-between">
                        {/* Logo/Brand and Desktop Navigation */}
                        <div className="flex items-center">
                            <a href="/" className="text-4xl font-orbital font-bold px-4 py-2">
                                Gains Trackers
                            </a>

                            {/* Desktop Navigation Items */}
                            <ul className="hidden lg:flex items-center">
                                <NavItem
                                    text={<a
                                        className={`${props.name.toLowerCase() === "nutrition" ? "text-info font-bold" : ""}`}
                                        href="/Nutrition">
                                        Nutrition
                                    </a>}
                                />
                                <NavItem
                                    text={<a
                                        className={`${props.name.toLowerCase() === "groups" ? "text-info font-bold " : ""}`}
                                        href="/Groups">
                                        Workout Groups
                                    </a>}
                                />
                                <NavItem
                                    text={<a
                                        className={`${props.name.toLowerCase() === "about-us" ? "text-info font-bold " : ""} `}
                                        href="/About-Us">
                                        About Us
                                    </a>}
                                />
                            </ul>
                        </div>

                        {/* Desktop Search Form */}
                        <div className="hidden lg:block">
                            <div className="flex items-center gap-2">
                                <input
                                    className="border-2 border-green-500 px-4 py-2 rounded-md text-white"
                                    id="navSearchDesktop"
                                    type="search"
                                    placeholder="Search"
                                    aria-label="Search"
                                />
                                <button
                                    className="border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-4 py-2 rounded-md transition-all"
                                    type="submit">
                                    Search
                                </button>
                            </div>
                        </div>

                        {/* Mobile menu button */}
                        <button
                            className="lg:hidden block text-white"
                            type="button"
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                            aria-label="Toggle menu">
                            <svg
                                className="w-6 h-6"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    d="M4 6h16M4 12h16M4 18h16"
                                />
                            </svg>
                        </button>
                    </div>

                    {/* Mobile Navigation Menu */}
                    <div
                        className={`${isMenuOpen ? "block" : "hidden"} lg:hidden mt-4`}
                    >
                        {/* Mobile Nav Links */}
                        <ul className="flex flex-col items-center">
                            <NavItem
                                text={<a
                                    className={`${props.name.toLowerCase() === "nutrition" ? "text-white font-bold underline" : "text-green-500"}`}
                                    href="/Nutrition">
                                    Nutrition
                                </a>}
                            />
                            <NavItem
                                text={<a
                                    className={`${props.name.toLowerCase() === "groups" ? "text-white font-bold underline" : "text-green-500"}`}
                                    href="/Groups">
                                    Workout Groups
                                </a>}
                            />
                            <NavItem
                                text={<a
                                    className={`${props.name.toLowerCase() === "about-us" ? "text-white font-bold underline" : "text-green-500"}`}
                                    href="/About-Us">
                                    About Us
                                </a>}
                            />
                        </ul>

                        {/* Mobile Search Form */}
                        <div className="mt-4 w-full">
                            <div className="flex flex-col items-center gap-2">
                                <input
                                    className="w-full max-w-md border-2 border-green-500 px-4 py-2 rounded-md text-black"
                                    id="navSearchMobile"
                                    type="search"
                                    placeholder="Search"
                                    aria-label="Search"
                                />
                                <button
                                    className="w-full max-w-md mt-2 border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-4 py-2 rounded-md transition-all"
                                    type="submit">
                                    Search
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        </header>
    );
}

export default Navbar;