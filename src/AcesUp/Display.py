#include "headers/Display.h"

Display::Display() {}

Display::~Display() {}

void Display::draw() {}

void Display::addCard() {}

void Display::removeCard() {}

static void Display::clearScreen()
{
    try {
        system("cls");
    } catch (int e) {
        cout << "\n\n\n";
    }
}

static void Display::printMainMenu()
{
    Display::clearScreen();

    cout << "Welcome to Aces Up!" << endl;
    cout << "Made by Patrick Barnum" << endl;
    cout << "2017, no rights reserved" << endl;
    cout << endl;
    cout << "Main Menu:" << endl;
    cout << "[N]ew game" << endl;
    cout << "[S]tatistics" << endl;
    cout << "[O]ptions" << endl;
    cout << "[A]bout" << endl;
    cout << "[Q]uit" << endl;
    cout << endl;
    cout << "Enter option: ";
}

static void Display::printGameMenu()
{
    Display::clearScreen();

    cout << "Welcome to Aces Up!" << endl;
    cout << "Made by Patrick Barnum" << endl;
    cout << "2017, no rights reserved" << endl;
    cout << endl;
    cout << "Main Menu:" << endl;
    cout << "[N]ew game" << endl;
    cout << "[S]tatistics" << endl;
    cout << "[O]ptions" << endl;
    cout << "[A]bout" << endl;
    cout << "[Q]uit" << endl;
    cout << endl;
    cout << "Enter option: ";
}
