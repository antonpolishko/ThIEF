# ThIEF 

> ThIEF: a Novel Tool for Tracking Genomic Features


## Installation

In order to have THiEF results you need to have gpsol intalled on your machine (part of the GLPK).


For Mac OS use homebrew: 
```
brew install homebrew/science/glpk
```

Clone this repo
```
git clone https://github.com/antonpolishko/ThIEF.git
```

## Usage

Input format is csv file with "," delimiter (you can change it in the process.py script in function ReadNucTable). Every line should correspond to a genetic feature and first column should be the location. Other columns are not essential for building tracks at this point. All files should have the same number of columns. 


Output format for the THiEF is simple table, every line is the resulting track of features (note that if you have multi column input files, i.e. <x1 a1 b1> and <y2 p2 q2>, then in the output the line corresponding to corresponding track will look like <x1 a1 b1 y2 p2 q2>). In case the track has "empty spots" (gaps), they are marked as "-1" (in multicolumn case it will be <-1 -1 -1>).

any questions send to: polishka@cs.ucr.edu

## License

MIT © [Anton Polishko](http://www.cs.ucr.edu/~polishka)
