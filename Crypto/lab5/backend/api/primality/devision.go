package primality

import (
	"math/big"
	"sync"
)

func runDevisionWorkers(n big.Int) bool {

	var mod big.Int

	if mod.Mod(&n, big.NewInt(2)).Cmp(big.NewInt(0)) == 0 {
		return false
	}

	THREADS := 5
	result := make(chan bool, THREADS)
	done := make(chan struct{})

	var wg sync.WaitGroup
	wg.Add(THREADS)

	var end big.Int
	end.Sqrt(&n).Add(&end, big.NewInt(1))
	step := big.NewInt(10)

	var i int64
	for i = 3; i < 12; i += 2 {
		go devisionWorker(&wg, n, *big.NewInt(i), end, *step, result, done)
	}

	for i = 0; i < 5; i++ {
		if <-result == false {
			return false
		}
	}
	return true
}

func devisionWorker(
	wg *sync.WaitGroup,
	n, start, end, step big.Int,
	result chan bool, done chan struct{},
) {
	defer wg.Done()

	var mod big.Int
	i := start
	for {
		select {
		case <-done:
			return
		default:
		}

		if i.Cmp(&end) >= 0 {
			break
		}

		if mod.Mod(&n, &i).Cmp(big.NewInt(0)) == 0 {
			result <- false
			close(done)
			return
		}
		i.Add(&i, &step)
	}
	result <- true
}
