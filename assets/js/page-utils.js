/**
 * page-utils.js
 * 
 * Proives useful utilities to have on page load, including adding event listeners to
 * a dark mode button, toggling mobile nav, and responding to user dark mode preferences.
 * 
 * Bradley McFadden
 * Written 2023-07-23
 */

"use strict";

const KEY_USES_DARK_MODE = "dark_mode";
const HIDDEN_CLASS = "hidden";
const DARK_MODE_CLASS = "dark-mode";

$( document ).ready(function() {
    console.log("ready");
    loadDarkMode();
    $("#mobile-site-nav-button").click(hideMobileItems);
    $("#dark-mode-button").click(() => {
        toggleDarkMode();
        persistDarkMode();
    });
    // Load current date in bottom of page
    const currentYear = new Date().getFullYear();
    console.log(`Year: ${currentYear}`);
    $("#current-year").html(`${currentYear}`);
})

window.onload = () => {
    console.log("onload");
    if (window.matchMedia) {
        var colorSchemeQuery = window.matchMedia("(prefers-color-scheme: dark)");
        colorSchemeQuery.addEventListener("change", updateColorScheme);
    }
}

function loadDarkMode() {
    if (localStorage.getItem(KEY_USES_DARK_MODE) === null) {
        console.log("local storage does not have dark mode");
    } else {
        let body = $("body");
        if (!body.hasClass(DARK_MODE_CLASS)) {
            body.addClass(DARK_MODE_CLASS);
        }
        console.log("local storage has dark mode");
    }
}

function persistDarkMode() {
    let body = $("body");
    if (body.hasClass(DARK_MODE_CLASS)) {
        localStorage.setItem(KEY_USES_DARK_MODE, "y");
    } else {
        localStorage.removeItem(KEY_USES_DARK_MODE);
    }
}

function hideMobileItems() {
    let navMenu = $("#mobile-site-nav-items");
    if (navMenu.hasClass(HIDDEN_CLASS)) {
        navMenu.removeClass(HIDDEN_CLASS);
    } else {
        navMenu.addClass(HIDDEN_CLASS);
    }
}

function toggleDarkMode() {
    console.log("toggle dark mode");
    let body = $("body");
    if (body.hasClass(DARK_MODE_CLASS)) {
        body.removeClass(DARK_MODE_CLASS);
    } else {
        body.addClass(DARK_MODE_CLASS);
    }
}

function getPreferredColorScheme() {
    if (window.matchMedia) {
        if (window.matchMedia("prefers-color-scheme: dark").matches) {
            return "dark";
        } else {
            return "light";
        }
    }
}

function updateColorScheme() {
    setColorScheme(getPreferredColorScheme());
}

function setColorScheme(scheme) {
    let body = $("body");
    let hasDarkMode = body.hasClass(DARK_MODE_CLASS);
    switch (scheme) {
        case "dark":
            if (!hasDarkMode) {
                body.addClass(DARK_MODE_CLASS);
            }
            break;
        case "light":
        default:
            if (hasDarkMode) {
                body.removeClass(DARK_MODE_CLASS);
            }
            break;
    }
}