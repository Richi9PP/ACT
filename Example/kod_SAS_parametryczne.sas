/* Analiza czasu trwania */
/* modele parametryczne */

/* ...*/;
/* przypisujemy bibliotekê my */;

LIBNAME my "...";

/* KOD 1 */;

PROC LIFEREG DATA=my.recid;
	MODEL week*arrest(0)=fin age race wexp mar paro prio
		/ DISTRIBUTION=GAMMA;
RUN;

/* dla ró¿nych rozk³adów bêdzie: 
DISTRIBUTION=EXPONENTIAL, 
DISTRIBUTION=WEIBULL, 
DISTRIBUTION=LNORMAL,
DISTRIBUTION=LLOGISTIC,
DISTRIBUTION=GAMMA. */


/* KOD 2 */

DATA recid;
SET my.recid;
IF educ = 2 THEN educ = 3;
IF educ = 6 THEN educ = 5;
RUN;

PROC LIFEREG DATA=recid;
	CLASS educ;
	MODEL week*arrest(0)=fin age race wexp mar paro
		prio educ / D=WEIBULL COVB;
RUN;
/* opcja COVB wyznacza macierz kowariancji*/;

/* KOD 3 */


PROC LIFEREG DATA=my.recid;
	MODEL week*arrest(0)=fin age race wexp mar paro prio
		/ DISTRIBUTION=GAMMA; PROBPLOT;
RUN;

/* dla ró¿nych rozk³adów bêdzie: 
DISTRIBUTION=EXPONENTIAL, 
DISTRIBUTION=WEIBULL, 
DISTRIBUTION=LNORMAL,
DISTRIBUTION=LLOGISTIC,
DISTRIBUTION=GAMMA. */


/* KOD 4 Left censoring */


PROC SORT DATA=my.recid OUT=recid2;
	BY DESCENDING arrest;
DATA recidlft;
	SET recid2;
	IF _N_ LE 30 THEN week = .;
RUN;

DATA recid3;
	SET recidlft;
		/* uncensored cases: */
	IF arrest=1 AND week ne . THEN DO;
		upper=week;
		lower=week;
	END;
		/* left-censored cases: */
	IF arrest=1 AND week = . THEN DO;
		upper=52;
		lower=.;
	END;
		/* right-censored cases: */
	IF arrest=0 THEN DO;
		upper=.;
		lower=52;
	END;
RUN;

PROC LIFEREG DATA=recid3;
	MODEL (lower,upper)=fin age race wexp mar paro prio
		/ D=WEIBULL;
RUN;

/* KOD 5 Interval censoring */

DATA recidint;
	SET my.recid;
		/* interval-censored cases: */
	IF arrest=1 THEN DO;
		upper=week;
		lower=week-.9999;
	END;
		/* right-censored cases: */
	IF arrest=0 THEN DO;
		upper=.;
		lower=52;
	END;
RUN;
PROC LIFEREG DATA=recidint;
	MODEL (lower, upper) = fin age race wexp mar paro prio
		/ D=WEIBULL;
RUN;

/* KOD 6 */

PROC LIFEREG DATA=my.recid;
	MODEL week*arrest(0)=fin age race wexp mar paro prio
		/ D=WEIBULL;
	OUTPUT OUT=a P=median STD=s;
RUN;

PROC PRINT DATA=a;
	VAR week arrest _prob_ median s;
RUN;

/* KOD 7 */

DATA quarter;
	SET my.recid;
	quarter=CEIL(week/13);
	DO j=1 TO quarter;
		time=13;
		event=0;
	IF j=quarter AND arrest=1 THEN DO;
		event=1;
		time=week-13*(quarter-1);
	END;
		OUTPUT;
	END;
RUN;


PROC LIFEREG DATA=quarter;
	CLASS j;
	MODEL time*event(0)=fin age race wexp mar paro prio j
		/ D=EXPONENTIAL COVB;
RUN;


/* end*/;
