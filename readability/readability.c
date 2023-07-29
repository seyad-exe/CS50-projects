#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    float lttrs = count_letters(text);
    float wrds = count_words(text);
    float snt = count_sentences(text);
    float L = lttrs / wrds * 100;// made to float for accurate calculations
    float S = snt / wrds * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index == 16)
    {
        printf("Grade 16\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
int count_letters(string text) //function for counting letter
{
    int no_letters = 0;
    for (int i = 0, len = strlen(text) ; i < len ; i++)
    {
        if (isalpha(text[i]))
        {
            no_letters += 1;
        }
    }
    return no_letters;//returns the number
}
int count_words(string text) //function for counting words
{
    int no_words = 0;
    for (int i = 0, len = strlen(text) ; i < len ; i++)
    {
        if (isspace(text[i]))
        {
            no_words++;
        }
    }
    return no_words += 1;//returns the number plus one
}
int count_sentences(string text) //function for counting sentences
{
    int no_sentences = 0;
    for (int i = 0, len = strlen(text) ; i < len ; i++)
    {
        if ((text[i] == 46) || (text[i] == 63) || (text[i] == 33))
        {
            no_sentences += 1;
        }
    }
    return no_sentences;//returns the number
}