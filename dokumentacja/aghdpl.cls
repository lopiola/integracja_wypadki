%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% File:     aghdpl.cls           (LaTeX Document class option "aghdpl")
%          
% Author:  Marcin Szpyrka     (mszpyrka@agh.edu.pl)
%          Grzegorz J. Nalepa (gjn@agh.edu.pl)
%          AGH University of Science and Technology, Krak�w, POLAND
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\message{*** [aghdpl.cls] ---  (MSz, GJN)  v2.0 <19.11.2013>  ***}       

\newif\ifpdflatex\pdflatexfalse
\NeedsTeXFormat{LaTeX2e} % 
\ProvidesClass{aghdpl} 
\DeclareOption{pdflatex}{\pdflatextrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}} 
\ProcessOptions\LoadClass[a4paper,openright]{report} 

\RequirePackage{times}
\RequirePackage[T1]{fontenc}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage[usenames]{color}
\RequirePackage{fancyhdr}
\RequirePackage{url}
\RequirePackage{titlesec}
\RequirePackage{tocloft}
\RequirePackage{polski}

\geometry{lmargin=20mm, rmargin=20mm, tmargin=20mm, bmargin=20mm, foot=10mm, head=10mm}
\definecolor{Green}{rgb}{0.1,0.5,0.1}

\def\shorttitlePL#1   {\gdef\@shorttitlePL{#1}}
\def\shorttitleEN#1   {\gdef\@shorttitleEN{#1}}
\def\shortauthor#1    {\gdef\@shortauthor{#1}}
\def\titlePL#1        {\gdef\@titlePL{#1}}
\def\titleEN#1        {\gdef\@titleEN{#1}}
\def\faculty#1      {\gdef\@faculty{#1}}
\def\thesistype#1   {\gdef\@thesistype{#1}}
\def\department#1   {\gdef\@department{#1}}
\def\degreeprogramme#1 {\gdef\@degreeprogramme{#1}}


%\bibliographystyle{abbrv}
\linespread{1.3}
\renewcommand{\labelitemi}{--}

%------------------------------------------------------------------------------


\def\thesisheaders{
\fancyfoot[LE,RO]{ZTIS, 2015}
}

\def\thesistable{
\begin{tabular}{p{45mm}l}
& {\itshape \@author}\\[-1mm]
\end{tabular}
}

\DeclareOption{en}{
\def\thesisheaders{
\fancyfoot[LE,RO]{ZTIS, 2015}
}

\def\thesistable{
\begin{tabular}{p{45mm}l}
Authors: & {\itshape \@author}\\[-1mm]
Supervisor: & {\itshape \@supervisor}\\
Manager: & {\itshape \@manager}\\
\end{tabular}
}
}

\ProcessOptions

\newcommand{\titlepages}{%

\newpage \titlepage 

\begin{center}
\vspace*{1.5cm}

\includegraphics[scale=0.6]{agh}

\vspace*{2mm}

{\sffamily{\large{\bfseries{\scshape Akademia G\'{o}rniczo-Hutnicza im. Stanis\l{}awa Staszica w Krakowie}}}

\vspace*{1mm}

{\small\bfseries \MakeUppercase{\@faculty}}}
\vspace*{3mm}

{\small{\MakeUppercase{\@department}}}
\vspace*{12mm}

{\small{\MakeUppercase{Wykonano w ramach:}}}

{\sffamily\Large \textbf{\@thesistype}}
\vspace*{9mm}

{\sffamily\Large\itshape Temat D: "Analiza przyczyn wypadk{\'o}w drogowych"}
\vspace*{1mm}

{\MakeUppercase{Wersja: \textbf{2.58}, 05.06.2015}}

\vspace*{3mm}

{\sffamily\Large\itshape Dokumentacja projektowa}
\vspace*{30mm}
\end{center}

\noindent
{\sffamily
\thesistable
}

\vspace*{3mm}

\centerline{lopiola@student.agh.edu.pl, bskiba@student.agh.edu.pl}

\vspace*{17mm}

\centerline{\small\sffamily Krak\'{o}w, \@date}

\clearpage \titlepage 

\setcounter{page}{2}
}


\pagestyle{fancy}
\renewcommand{\chaptermark}[1]{\markboth{\thechapter.\ #1}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection.\ #1}}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}
\fancyhf{}
\fancyhead{}
%\fancyhead[L]{\slshape{\small \rightmark}}
\fancyhead[RE,LO]{\small \@shortauthor\quad\textit{Temat D: Przyczyny wypadk{\'o}w drogowych}}
%\fancyhead[R]{\bfseries \thepage}
\fancyhead[RO,LE]{\bfseries \thepage}

\thesisheaders

\frenchspacing
\sloppy 
\widowpenalty     9999 
\clubpenalty      9999 
\flushbottom

%---------------------------------------------------------------------------
% Ustawienia parametr�w dla tytu��w rozdzia��w, podrozdzia��w, itd.
%---------------------------------------------------------------------------


\titleformat{\chapter}[block]
{\bfseries\LARGE}{\filright \LARGE\thechapter. }{0ex}{}
%odst�py: lewy, g�ra, d��
\titlespacing{\chapter}{0pt}{17mm}{19mm}
\titleformat{\section}[block]
{\bfseries\Large}{\filright \Large\thesection. }{0ex}{}
\titlespacing{\section}{7mm}{8mm plus 0mm minus 1mm}{4mm plus 0mm minus 1mm}
\titleformat{\subsection}[block]
{\bfseries\large}{\filright \large\thesubsection. }{0ex}{}
\titlespacing{\subsection}{7mm}{6mm}{2.5mm}
\titleformat{\subsubsection}[block]
{\bfseries\normalsize}{\filright \normalsize\thesubsubsection. }{0ex}{}
\titlespacing{\subsubsection}{7mm}{3mm}{1.5mm}

%---------------------------------------------------------------------------
% Ustawienia parametr�w generowania spisu tre�ci i spisu rysunk�w
%---------------------------------------------------------------------------

\renewcommand{\cfttoctitlefont}{\bfseries\Large}
\renewcommand{\cftbeforetoctitleskip}{20mm}
\renewcommand{\cftaftertoctitleskip}{19mm}
\renewcommand{\cftchapleader}{\cftdotfill{\cftdot}}
\renewcommand{\cftsecleader}{\cftdotfill{\cftdot}}
\renewcommand{\cftsubsecleader}{\cftdotfill{\cftdot}}
\renewcommand{\cftchapaftersnum}{.}
\renewcommand{\cftsecaftersnum}{.}
\renewcommand{\cftsubsecaftersnum}{.}
\setlength{\cftparskip}{2pt}
\setlength{\cftbeforechapskip}{0mm}
\renewcommand{\cftchappagefont}{\normalsize}

% Smaller spaces between items of itemize
\usepackage{xpatch}
\xpatchcmd{\itemize}
  {\def\makelabel}
  {\ifnum\@itemdepth=1\relax
     \setlength\itemsep{-14pt}% separation for first level
     \setlength\parskip{-6pt}
     \setlength\parsep{-6pt}
   \else
     \ifnum\@itemdepth=2\relax
       \setlength\itemsep{-14pt}% separation for second level
       \setlength\parskip{-6pt}
       \setlength\parsep{-6pt}
     \else
       \ifnum\@itemdepth=3\relax
         \setlength\itemsep{-14pt}% separation for third level
         \setlength\parskip{-6pt}
         \setlength\parsep{-6pt}
       \else
         \setlength\itemsep{-14pt}% separation for fourth level
         \setlength\parskip{-6pt}
         \setlength\parsep{-6pt}
   \fi\fi\fi\def\makelabel
  }
 {}
 {}