#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#define N 5867
#define N_DATA_COL 3138

typedef struct Radius
{
	int C[N][N];
	int M[N][N];
	int U[N][N];
} Radius;

typedef struct Distance
{
	int id;
	double d;
} Distance;

typedef struct County 
{
	char c;
	int pop;
	double lat;
	double lng;
	int valid;
} County;

County *COUNTIES;
Radius *RADIUS;

int compareDistance(Distance *x, Distance *y)
{
	double temp = x->d - y->d;
	if (temp > 0)
		return 1;
	else if (temp < 0)
		return -1;
	else
		return 0;
}

double distance(County *x, County *y) 
{
	double xLat = x->lat;
	double xLng = x->lng;
	double yLat = y->lat;
	double yLng = y->lng;
	double earth = 6371;
	double degToRad = M_PI / 180;
	double dLat = (xLat - yLat) * degToRad;
	double dLng = (xLng - yLng) * degToRad;
	double sindLat = sin(dLat / 2);
	double sindLng = sin(dLng / 2);
	double a = pow(sindLat, 2) + pow(sindLng, 2) * cos(xLat * degToRad) * cos(yLat * degToRad);
	double c = 2 * atan2(sqrt(a), sqrt(1 - a));
	double distance = earth * c;
	return distance;
}

void loadCounties(County *counties)
{
	COUNTIES = counties;
	RADIUS = (Radius*) malloc(sizeof(Radius));
	Distance *distances = (Distance*) malloc(sizeof(Distance) * N);

	int i;
	for (i = 0 ; i < N ; i++)
	{
		if (!COUNTIES[i].valid || COUNTIES[i].c != 'U')
			continue;
		
		int j;
		for (j = 0 ; j < N ; j++)
		{
			distances[j].id = j;
			distances[j].d = distance(&COUNTIES[i], &COUNTIES[j]);
		}

		qsort(distances, N, sizeof(Distance), compareDistance);	
		
		int lastId, thisId = distances[0].id;
		RADIUS->C[i][thisId] = 0;
		RADIUS->M[i][thisId] = 0;
		RADIUS->U[i][thisId] = 0;

		for (j = 1 ; j < N ; j++)
		{
			lastId = thisId;
			thisId = distances[j].id;
			
			if (i == lastId || !COUNTIES[thisId].valid)
			{
				RADIUS->C[i][thisId] = 0;
				RADIUS->M[i][thisId] = 0;
				RADIUS->U[i][thisId] = 0;
				if (!COUNTIES[thisId].valid)
					thisId = lastId;
				continue;
			}

			RADIUS->C[i][thisId] = RADIUS->C[i][lastId];
			RADIUS->M[i][thisId] = RADIUS->M[i][lastId];
			RADIUS->U[i][thisId] = RADIUS->U[i][lastId];
			
			if (COUNTIES[lastId].c == 'C')
				RADIUS->C[i][thisId] += COUNTIES[lastId].pop;
			else if (COUNTIES[lastId].c == 'M')
				RADIUS->M[i][thisId] += COUNTIES[lastId].pop;
			else
				RADIUS->U[i][thisId] += COUNTIES[lastId].pop;
		}
	}

	free(distances);
}

void probability(double P[N][N], double gammaC, double gammaM)
{
	int mi, mj, cij, mij, uij;
	double gamma, p, total;
	int i;
	for (i = 0 ; i < N ; i++)
	{
		if (!COUNTIES[i].valid || COUNTIES[i].c != 'U')
			continue;
		
		total = 0;
		int j;
		for (j = 0 ; j < N ; j++)
		{
			if (i == j || !COUNTIES[j].valid)
				continue;

			mi = COUNTIES[i].pop;
			mj = COUNTIES[j].pop;
			cij = RADIUS->C[i][j];
			mij = RADIUS->M[i][j];
			uij = RADIUS->U[i][j];
			gamma = 1.0;
			if (COUNTIES[j].c == 'C')
				gamma = gammaC;
			else if (COUNTIES[j].c == 'M')
				gamma = gammaM;

			p = mi * ( 1.0 / ( mi + uij + gammaC * cij + gammaM * mij ) 
				- 1.0 / ( mi + uij + gammaC * cij + gammaM * mij + gamma * mj ) );
			
			P[i][j] = p;
			
			total += p;
		}
		
		// Normalize probability
		for (j = 0 ; j < N ; j++)
			P[i][j] = P[i][j] / total;
	}
}

void flux(double F[N][N], double T[N][N_DATA_COL], double include[N_DATA_COL], double P[N][N])
{
	int i;
	for (i = 0 ; i < N ; i++)
	{
		double Ti = 0;
		int j;
		for (j = 0 ; j < N_DATA_COL ; j++)
		{
			if (include[j])
				Ti += T[i][j];
		}

		for (j = 0 ; j < N ; j++)
			F[i][j] = Ti * P[i][j];
	}
}

double **probabilityToData(double oldP[N][N])
{
	double** P;
	P = (double**) malloc(N * sizeof(double*));  
	int i;
	for (i = 0 ; i < N ; i++)
		P[i] = (double*) malloc(N_DATA_COL * sizeof(double));

	for (i = 0 ; i < N ; i++)
	{
		if (COUNTIES[i].c != 'U')
			continue;
		
		int dataColumn = 0;
		double cProb = 0, mProb = 0;
		int j;
		for (j = 0 ; j < N ; j++)
		{
			double p = oldP[i][j];
			if (COUNTIES[j].c == 'C')
				cProb += p;
			else if (COUNTIES[j].c == 'M')
				mProb += p;
			else if (COUNTIES[j].c == 'U')
			{
				P[i][dataColumn] = p;
				dataColumn++;
			}
		}
		P[i][N_DATA_COL - 2] = cProb;
		P[i][N_DATA_COL - 1] = mProb;
	}
	return P;
}

double logLikelihood(double T[N][N_DATA_COL], double oldP[N][N])
{
	double **P = probabilityToData(oldP);

	double L = 0;
	int i;
	for (i = 0 ; i < N ; i++)
	{
		if (COUNTIES[i].c != 'U')
			continue;
		
		int j;
		for (j = 0 ; j < N_DATA_COL ; j++)
		{
			if (P[i][j] != 0)
				L += T[i][j] * log(P[i][j]);
		}
	}
	
	for (i = 0 ; i < N ; i++)
		free(P[i]);
	free(P);

	return -L;
}