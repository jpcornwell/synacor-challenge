#include <stdio.h>
 
int verifier(int m, int n, int k)
{
   if (m == 2) return (n * (k + 1) + 2 * k + 1) % 32768;
   if (n == 0) return (verifier(m - 1, k, k)) % 32768;
   return (verifier(m - 1, verifier(m, n - 1, k), k)) % 32768;
}
 
int main()
{
   int m = 4;
   int n = 1;

   for (int k = 1; k < 32768; k++) {
      if (verifier(m, n, k) == 6) printf("%d\n", k);
   }
 
   return 0;
}
