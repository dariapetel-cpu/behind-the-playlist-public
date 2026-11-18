% =====================================================================
%  behind-the-playlist.cls: document class for „מאחורי הפלייליסט"
%  Engine: LuaLaTeX (+ Biber, biblatex-ieee). Replaces book/style.sty (XeLaTeX).
%
%  CHANGELOG
%   v1.1 2026-11-18  QA round 1 (Fixer, finding D1-03): bibliography URLs no
%     longer break inside "https://" (was "https:" | "//host"); ':' and the
%     two '/' after it are unbreakable. Breaks at other / . - etc. unchanged.
%   v1.0 2026-11-18  First class version (Prompt 18):
%     - XeLaTeX/polyglossia/bidi → LuaLaTeX/babel: bidi=basic,
%       layout=graphics.lists, onchar=ids fonts (settings proven in
%       tests/lualatex-smoke and tests/font-compare).
%     - Fonts: Pairing A (bundled, OFL): Frank Ruhl Libre (Hebrew body),
%       Heebo (headings), Libertinus Serif (Latin, italics, math roman).
%     - Bibliography: biblatex style=ieee, Hebrew heading „מקורות",
%       LTR English entries, DOI-only for DOI entries.
%     - The five in-chapter layout edits from the audit (A2-13) are now
%       class commands: \besidetable, \sidebyside, comparisontable,
%       herefigure, Latin in headings (automatic; \enhead kept as no-op).
%     - Design unchanged: charcoal/green/pink palette, boxes, "רצועה"
%       chapter openers with equalizer, playback footer.
%
%  COMMAND LIST (writer interface): see the WRITER INTERFACE block below.
% =====================================================================
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{behind-the-playlist}[2026/11/18 v1.1 Behind the Playlist book class]
\newcommand{\bookclassversion}{v1.1 (2026/11/18)}

\LoadClass[11pt,a4paper,oneside,openany]{book}

% ---------- page ----------------------------------------------------
\RequirePackage[a4paper,top=2.6cm,bottom=3.0cm,inner=2.5cm,outer=2.5cm,
  headsep=0.8cm,footskip=1.3cm]{geometry}
\RequirePackage{setspace}
\setstretch{1.22}
\setlength{\parskip}{0.45em}
\setlength{\parindent}{0pt}
\raggedbottom

% ---------- packages -------------------------------------------------
\RequirePackage{amsmath}
\RequirePackage[table]{xcolor}
\RequirePackage{graphicx}
\RequirePackage{array,tabularx,booktabs}
\RequirePackage{caption}
\RequirePackage{enumitem}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{zref-totpages}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,positioning,calc,shapes.misc}
\RequirePackage[skins,breakable]{tcolorbox}
\RequirePackage[style=english,autostyle=false]{csquotes}
\RequirePackage[hidelinks]{hyperref}

% ---------- languages & bidi (LuaLaTeX) -------------------------------
% bidi=basic: Unicode bidi algorithm; layout=graphics: TikZ node text placed and
% mirrored correctly; layout=lists: LTR lists (bibliography) indented on the
% correct side inside the RTL document; layout=tabular: tables run right to left
% (first column on the right, as in the XeLaTeX book); onchar=ids fonts: Latin runs switch to
% the English font automatically (no missing glyphs, brackets mirrored).
\RequirePackage[bidi=basic,layout=graphics.lists.tabular]{babel}
\babelprovide[main,import,onchar=ids fonts]{hebrew}
\babelprovide[import,onchar=ids fonts,hyphenrules=nohyphenation]{english} % no mid-word breaks of English inside Hebrew lines

% ---------- fonts: Pairing A (bundled in book/fonts/, OFL 1.1) --------
\newcommand{\bookfontdir}{fonts/}
\babelfont{rm}[Path=\bookfontdir LibertinusSerif/,Extension=.otf,UprightFont=*-Regular,
  ItalicFont=*-Italic,BoldFont=*-Bold,BoldItalicFont=*-BoldItalic,Scale=1.03]{LibertinusSerif}
\babelfont[hebrew]{rm}[Path=\bookfontdir FrankRuhlLibre/,Extension=.ttf,UprightFont=*-Regular,
  BoldFont=*-Bold,Scale=0.96]{FrankRuhlLibre}
\babelfont{sf}[Path=\bookfontdir Heebo/,Extension=.ttf,UprightFont=*-Regular,BoldFont=*-Bold,Scale=0.97]{Heebo}
\babelfont[hebrew]{sf}[Path=\bookfontdir Heebo/,Extension=.ttf,UprightFont=*-Regular,BoldFont=*-Bold,Scale=0.97]{Heebo}
\setmathrm{LibertinusSerif}[Path=\bookfontdir LibertinusSerif/,Extension=.otf,
  UprightFont=*-Regular,ItalicFont=*-Italic,BoldFont=*-Bold]
\newcommand{\headfont}{\sffamily}          % headings, tags, captions: Heebo (Hebrew + Latin)
\providecommand{\hebrewfont}{\rmfamily}    % kept for main.tex (cover details)

% ---------- bibliography: IEEE ----------------------------------------
\RequirePackage[backend=biber,style=ieee,isbn=false,sortcites=true]{biblatex}
\setcounter{biburlnumpenalty}{0}   % URLs break only at / . - ; no stretched gaps
\setcounter{biburlucpenalty}{0}
\setcounter{biburllcpenalty}{0}
% v1.1 (QA round 1, D1-03): no URL break inside "scheme://", so "https://" stays
% with the host. ':' is no longer a break point (set as an ordinary character),
% and the two '/' right after a ':' are ordinary too; every other '/' keeps its
% normal break (penalty biburlbreakpenalty). Side effect: after a ':' elsewhere
% in a URL the next two '/' do not break (none of our sources has such a URL).
\appto\biburlsetup{%
  \def\UrlBigBreaks{\do\-}%
  \def\btp@urlslashes{0}%
  \appto\UrlSpecials{%
    \do\:{\mathchar`\:\def\btp@urlslashes{2}}%
    \do\/{\ifnum\btp@urlslashes>\z@
            \mathchar`\/\edef\btp@urlslashes{\the\numexpr\btp@urlslashes-1}%
          \else\mathchar\numexpr"2000+`\/\relax\fi}}}
\AtBeginBibliography{\raggedright}
% Entries with a DOI print the DOI only (URL + access date redundant); web-only keep both.
\DeclareSourcemap{\maps[datatype=bibtex]{\map{
  \step[fieldsource=doi,final]
  \step[fieldset=url,null]
  \step[fieldset=urldate,null]}}}
% Hebrew heading, English LTR entries (PRD §6 decision), all inside the margins.
\newcommand{\printbookbibliography}{%
  \chapter*{מקורות}\addcontentsline{toc}{chapter}{מקורות}\markboth{מקורות}{}%
  \begin{otherlanguage}{english}\printbibliography[heading=none]\end{otherlanguage}}

% ---------- palette ------------------------------------------------------
% Contrast (WCAG, measured): charcoal on pagebg 16.7:1, on green 9.8:1, on pink 5.4:1.
% Green (1.7:1) and pink (3.1:1) on pagebg are not used for text.
\definecolor{charcoal}{HTML}{121212}
\definecolor{brandgreen}{HTML}{1ED760}
\definecolor{brandpink}{HTML}{FF2E88}
\definecolor{pagebg}{HTML}{F2F2F2}
\definecolor{muted}{HTML}{555555}
\definecolor{rulegrey}{HTML}{CFCFCF}
\colorlet{greensoft}{brandgreen!16!white}
\colorlet{pinksoft}{brandpink!9!white}
\pagecolor{pagebg}
\AtBeginDocument{\color{charcoal}\let\default@color\current@color}

% ---------- RTL helpers (LuaLaTeX equivalents of the XeLaTeX rules) ---
% In LuaLaTeX, babel's layout=graphics handles TikZ node direction, so the XeTeX
% \beginR…\endR wrapper (and its white-text side effect) is no longer needed.
\tikzset{heb/.style={}}                       % kept so old figures still compile
\newcommand{\hebcolor}[2]{\textcolor{#1}{#2}}  % kept for figures/cover
\providecommand{\LR}[1]{\babelsublr{#1}}       % left-to-right unit (IDs, dates)

% ---------- chapter openers: "רצועה 01" + equalizer -------------------
\newcommand{\eqbars}[1]{%
  \begin{tikzpicture}[baseline=0pt]
    \foreach \i in {0,...,17}{
      \pgfmathsetmacro{\h}{0.12+0.5*abs(sin(37*\i+53*#1))}
      \pgfmathsetmacro{\c}{mod(\i,5)==2 ? "brandpink" : "brandgreen"}
      \fill[\c] (\i*0.17,0) rectangle ++(0.09,\h);}
  \end{tikzpicture}}
\newcommand{\tracklabel}[1]{\textcolor{charcoal}{\headfont\small רצועה\enspace\ifnum#1<10 0\fi#1}}
\titleformat{\chapter}[display]
  {\headfont\color{charcoal}}
  {\tracklabel{\thechapter}\hfill\eqbars{\thechapter}}
  {6pt}
  {\bfseries\fontsize{24}{30}\selectfont}
  [\vspace{4pt}{\color{brandgreen}\titlerule[1.2pt]}]
\titleformat{name=\chapter,numberless}[display]
  {\headfont\color{charcoal}}{}{0pt}
  {\bfseries\fontsize{24}{30}\selectfont}
  [\vspace{4pt}{\color{brandgreen}\titlerule[1.2pt]}]
\titlespacing*{\chapter}{0pt}{-18pt}{16pt}
\titleformat{\section}{\headfont\bfseries\large\color{charcoal}}{}{0pt}{}
\titlespacing*{\section}{0pt}{12pt}{4pt}
\setcounter{secnumdepth}{0}
\setcounter{tocdepth}{0}

% ---------- playback footer ---------------------------------------------
\newcommand{\playerbar}{%
  \begin{tikzpicture}
    \pgfmathsetmacro{\tot}{max(\ztotpages,1)}
    \pgfmathsetmacro{\pf}{min(\thepage/\tot,1)}
    \draw[rulegrey,line width=1.4pt,line cap=round] (1.1cm,0) -- (\textwidth-1.1cm,0);
    \draw[brandgreen,line width=1.6pt,line cap=round]
      (\textwidth-1.1cm,0) -- ($(\textwidth-1.1cm,0)-(\pf*\textwidth-\pf*2.2cm,0)$);
    \fill[brandpink] ($(\textwidth-1.1cm,0)-(\pf*\textwidth-\pf*2.2cm,0)$) circle (2.8pt);
    \node[font=\sffamily\scriptsize,text=charcoal,anchor=east] at (\textwidth,0) {\thepage};
    \node[font=\sffamily\scriptsize,text=muted,anchor=west] at (0,0) {\ztotpages};
  \end{tikzpicture}}
\pagestyle{fancy}
\fancyhf{}
% Under babel (RTL), fancyhdr's L/R are the opposite physical sides of the XeLaTeX book:
% [L] is printed on the RIGHT. Book title on the right, chapter title on the left (as before).
% Header/footer are always typeset in Hebrew: a page break inside the English bibliography
% otherwise builds the footer LTR (page numbers reversed, bar mirrored; found 2026-11-18, p. 19).
\newcommand{\inhebrew}[1]{\foreignlanguage{hebrew}{#1}}
\fancyhead[L]{\inhebrew{\headfont\footnotesize\color{muted}מאחורי הפלייליסט}}
\fancyhead[R]{\inhebrew{\headfont\footnotesize\color{muted}\leftmark}}
\fancyfoot[C]{\inhebrew{\playerbar}}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\inhebrew{\playerbar}}\renewcommand{\headrulewidth}{0pt}}

% ---------- captions ---------------------------------------------------
\DeclareCaptionFont{charcoal}{\color{charcoal}}
\captionsetup{font={small,sf,charcoal},labelfont={bf,color=charcoal},labelsep=colon,
  justification=centering,skip=6pt}

% ---------- lists --------------------------------------------------------
\setlist{itemsep=2pt,topsep=4pt}
\setlist[itemize]{label={\tikz[baseline=-0.55ex]\fill[brandpink] (0,0) circle (1.8pt);}}

% ---------- boxes ---------------------------------------------------------
\newcommand{\boxtitle}[3][]{{\headfont\bfseries\color{#2}#3}\ifx\relax#1\relax\else\hfill#1\fi\par\smallskip}
\tcbset{bookbase/.style={enhanced,breakable,boxrule=0pt,arc=1.6mm,coltext=charcoal,coltitle=charcoal,
  left=4mm,right=5mm,top=3mm,bottom=3mm,before skip=10pt,after skip=10pt}}
\DeclareRobustCommand{\tagpill}[1]{\tikz[baseline=(t.base)]\node[draw=muted,dashed,rounded corners=2pt,
  inner xsep=3.5pt,inner ysep=2.5pt,font=\headfont\footnotesize](t){\textcolor{muted}{#1}};}

% ===================== WRITER INTERFACE =====================
% \begin{scene} … \end{scene}                 fictional scene (titled "סצנה", tagged "בדיוני")
% \begin{inshort} … \end{inshort}             "בקצרה" takeaways (green rule)
% \begin{lab}{<title>} … \end{lab}            "מעבדה" formula/worked example, tagged "דוגמה לימודית"
% \begin{realitycheck} … \end{realitycheck}   "רגע, זה אמיתי?" (pink rule)
% \fictional, \educational                    inline tags
% \term{מונח}{English term}                   first use of a term: bold Hebrew + (English)
% \en{English text}                           English words inside Hebrew text
% \enhead{English}                            no-op since v1.0 (Latin in headings is automatic)
% \cite[<postnote>]{keys}                     IEEE citation, printed as one LTR [n] unit
% --- layout commands (replace the former in-chapter edits, audit A2-13) ---
% \besidetable{<tabular>}{<text>}             small table on the right, its intro text on the left
% \sidebyside{<right column>}{<left column>}  two equal columns (e.g. two worked calculations)
% \begin{comparisontable}{<caption>}{<label>}{<tabularx preamble>} … \end{comparisontable}
%                                             full-width table placed here, ragged flush-right cells
% \begin{herefigure} … \end{herefigure}       figure placed right here (after its intro text)
% column type H                                Hebrew cell flush right in RTL tables (use instead of r)
\newtcolorbox{scene}{bookbase,colback=white,borderline east={2pt}{0pt}{muted,dashed},
  before upper={\boxtitle[\tagpill{בדיוני}]{charcoal}{סצנה}}}
\newtcolorbox{inshort}{bookbase,colback=greensoft,borderline east={3.5pt}{0pt}{brandgreen},
  before upper={\boxtitle{charcoal}{בקצרה}}}
\newtcolorbox{lab}[1]{bookbase,colback=white,borderline east={3.5pt}{0pt}{charcoal},
  before upper={\boxtitle[\tagpill{דוגמה לימודית}]{charcoal}{מעבדה: #1}}}
\newtcolorbox{realitycheck}{bookbase,colback=pinksoft,borderline east={3.5pt}{0pt}{brandpink},
  before upper={\boxtitle{charcoal}{רגע, זה אמיתי?}}}
\DeclareRobustCommand{\fictional}{\tagpill{נתונים בדיוניים}}
\DeclareRobustCommand{\educational}{\tagpill{דוגמה לימודית}}
\newcommand{\term}[2]{\textbf{\textcolor{charcoal}{#1}}~(\en{#2})}
\newcommand{\en}[1]{\foreignlanguage{english}{#1}}
\newcommand{\enhead}[1]{#1}
\AtBeginDocument{%
  \let\bookorigcite\cite
  \RenewDocumentCommand{\cite}{o m}{\babelsublr{\IfValueTF{#1}{\bookorigcite[#1]{#2}}{\bookorigcite{#2}}}}}

% ---------- layout commands (audit A2-13: fixes live in the class, not in chapters)
% (1) Chapter 3: data table beside its introduction.
\newcommand{\besidetable}[2]{\par\noindent
  \begin{minipage}[c]{0.38\linewidth}\centering #1\end{minipage}\hfill
  \begin{minipage}[c]{0.58\linewidth}#2\end{minipage}\par\medskip}
% (2) Chapter 3: two calculations side by side.
\newcommand{\sidebyside}[2]{\par\noindent
  \begin{minipage}[t]{0.485\linewidth}#1\end{minipage}\hfill
  \begin{minipage}[t]{0.485\linewidth}#2\end{minipage}\par\medskip}
% (3)+(4) Chapter 4: comparison table kept under its section, ragged flush-right X cells.
\newcommand{\bookraggedcell}{\raggedright}   % measured: flush-right in RTL under babel/LuaTeX (see PRD §6)
% \table…\endtable (not \begin{table}) keeps \@currenvir = comparisontable, which
% tabularx needs to find the end of its body.
\newenvironment{comparisontable}[3]
  {\table[h!]\centering\caption{#1}\label{#2}%
   \renewcommand{\tabularxcolumn}[1]{>{\bookraggedcell\arraybackslash}p{##1}}%
   \tabularx{\textwidth}{#3}}
  {\endtabularx\endtable}
% (6) RTL table alignment: with babel layout=tabular (LuaLaTeX), column type `l` sets cells
% flush toward the RIGHT margin (the reading start) and `r` flush left, i.e. the opposite of
% the XeLaTeX/bidi book. `H` names the Hebrew flush-right column explicitly (measured 2026-11-18).
\newcolumntype{H}{l}
% (5) Chapter 6: figure placed right after its introduction.
\newenvironment{herefigure}{\begin{figure}[h!]}{\end{figure}}

\endinput
