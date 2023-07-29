#include "helpers.h"
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float B = image[i][j].rgbtBlue;
            float G = image[i][j].rgbtGreen;
            float R = image[i][j].rgbtRed;
            int avg = round((B + G + R) / 3);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int s_imageRed = round(.189 * image[i][j].rgbtBlue + .769 * image[i][j].rgbtGreen + .393 * image[i][j].rgbtRed);
            int s_imageGreen = round(.168 * image[i][j].rgbtBlue + .686 * image[i][j].rgbtGreen + .349 * image[i][j].rgbtRed);
            int s_imageBlue = round(.131 * image[i][j].rgbtBlue + .534 * image[i][j].rgbtGreen + .272 * image[i][j].rgbtRed);
            if (s_imageRed > 255)
            {
                s_imageRed = 255;
            }
            if (s_imageBlue > 255)
            {
                s_imageBlue = 255;
            }
            if (s_imageGreen > 255)
            {
                s_imageGreen = 255;
            }
            image[i][j].rgbtBlue = s_imageBlue;
            image[i][j].rgbtRed = s_imageRed;
            image[i][j].rgbtGreen = s_imageGreen;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temporary = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temporary;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temporary[height][width];
    //copying into temp image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temporary[i][j] = image[i][j];
        }
    }
    //going through image again
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //values for all the rgb values of surrounding pixels
            int totalred, totalgreen, totalblue;
            totalred = totalgreen = totalblue = 0;
            float counter = 0.00;//keeps track of valid pixels

            for (int x = -1 ; x < 2; x++)
            {
                for (int y = -1 ; y < 2; y++)
                {
                    //for loops used to go to surrounding of i,j pixel
                    int cursorX = i + x;
                    int cursorY = j + y;
                    //this is the surrounding pixels
                    if (cursorX < 0 || cursorY < 0 || cursorX > (height - 1) || cursorY > (width - 1)) //if condition checking for valid pixel
                    {
                        continue;
                    }//adding up the rgb values
                    totalred += image[cursorX][cursorY].rgbtRed;
                    totalgreen += image[cursorX][cursorY].rgbtGreen;
                    totalblue += image[cursorX][cursorY].rgbtBlue;

                    counter++;//updating count for valid pixels
                }
                temporary[i][j].rgbtRed = round(totalred / counter);
                temporary[i][j].rgbtGreen = round(totalgreen / counter);
                temporary[i][j].rgbtBlue = round(totalblue / counter);
            }
        }
    }
    //copying temp into OG image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temporary[i][j].rgbtRed;
            image[i][j].rgbtGreen = temporary[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temporary[i][j].rgbtBlue;
        }
    }
    return;
}
