from sympy           import isprime, randprime
from multiprocessing import cpu_count, Pool
from argparse        import ArgumentParser
#from colorama.ansi   import clear_screen
from sys             import exit, argv
from time            import sleep
from tqdm            import tqdm
#from colorama        import init

def worker(args):
    num_primes, bits, process_id = args
    prime_set = set()
    try:
        for _ in tqdm(range(num_primes), desc=f"\rProceso {process_id}", position=process_id + 1, leave=True):
            candidate = randprime(2**(bits-1), 2**bits)
            if isprime(candidate): prime_set.add(candidate)
    except KeyboardInterrupt: pass
    return list(prime_set)

def generate_large_primes_parallel(num_primes, bits, utilization_percentage=80):
    if cpu_count() > num_primes: num_processes = num_primes
    else: num_processes = int(cpu_count() * utilization_percentage / 100)
    print(num_processes)
    args_list = [(num_primes // num_processes, bits, i) for i in range(num_processes)]
    with Pool(processes=num_processes) as pool: results = list(pool.imap(worker, args_list))

    final_primes = [prime for result in results for prime in result]
    print("\nGeneración de primos completada.")

    return final_primes



if __name__ == '__main__':
    parser = ArgumentParser(
                prog = __doc__,
                description = """
                    Esta es una herramienta que permite generar una serie
                    de numeros primos de una longitud de bit's deseada usando
                    multi proceso. Se puede utilizar para generar claves criptograficas
                """,
                epilog="""
                """
            )

    parser.add_argument(
                            "-np",
                            "--num-primes",        
                            help="cantidad de numeros primos a generar", 
                            type=int,
                            default=0
                        )
    parser.add_argument(
                            "-b",
                            "--bits",        
                            help="longitud de los numeros primos a generar en bit's", 
                            type=int,
                            default=0
                        )
    parser.add_argument(
                            "-up",
                            "--utilization-percentage",        
                            help="porcentaje de cores a usar para generar numeros primos, una mayor numero se traduce en una velocidad mayor de generacion. Tener cudidado con la temperatura de la CPU. Por defecto se usa 80%%", 
                            type=int,
                            default=80
                        )
    """parser.add_argument(
                            "-sb",
                            "--show-bar",        
                            help="mostrar barra de carga para la generacion", 
                            type=bool,
                            default=True
                        )"""

    #init(convert=True)
    #print(clear_screen())

    if len(argv) <= 1:
        parser.print_help()
        exit(1)
        
    parser = parser.parse_args()

    # Definir la cantidad de números primos que deseas generar y la cantidad de bits
    num_primes = parser.num_primes
    if not parser.num_primes:
        print("No ingreso la cantidad de numeros primos a generar")
        exit(1)
    bits = parser.bits
    if not bits:
        print("No ingreso la longitud de los numeros primos a generar")
        exit(1)
    
    utilization_percentage = parser.utilization_percentage

    print(f"\nNumero de procesos a usar: {int(cpu_count() * utilization_percentage / 100)}\n\n")
    sleep(3)

    # Generar números primos grandes utilizando el algoritmo de Miller-Rabin en paralelo
    large_primes_parallel = generate_large_primes_parallel(num_primes, bits, utilization_percentage)

    # Imprimir la lista de primos
    print("\r\n\n\n{")
    for prime in large_primes_parallel:
        print("\t" + str(prime))
    print("}")
    


