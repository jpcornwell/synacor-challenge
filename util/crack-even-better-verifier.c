#include <stdio.h>
 
int verifier(int m, int n, int k)
{
   int temp;
   if (m == 3) {
      temp = k * k + 3 * k + 1;
      for (int i = 0; i < n; i++) {
         temp = temp * (k + 1) + 2 * k + 1;
      }
      return temp % 32768;
   }
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
