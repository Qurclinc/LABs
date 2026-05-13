package primality

import (
	"context"
	"math/big"
	"sync"
)

func runDevisionWorkers(ctx context.Context, n big.Int) bool {
	var mod big.Int
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	if mod.Mod(&n, big.NewInt(2)).Cmp(big.NewInt(0)) == 0 {
		return false
	}

	THREADS := 5
	result := make(chan bool, THREADS)

	var wg sync.WaitGroup
	wg.Add(THREADS)

	var end big.Int
	end.Sqrt(&n).Add(&end, big.NewInt(1))
	step := big.NewInt(10)

	var i int64
	for i = 3; i < 12; i += 2 {
		go devisionWorker(&wg, ctx, cancel, n, *big.NewInt(i), end, *step, result)
	}

	for i = 0; i < int64(THREADS); i++ {
		if <-result == false {
			return false
		}
	}
	return true
}

func devisionWorker(
	wg *sync.WaitGroup,
	ctx context.Context,
	cancel context.CancelFunc,
	n, start, end, step big.Int,
	result chan bool,
) {
	defer wg.Done()

	var mod big.Int
	zero := big.NewInt(0)

	i := start
	for {
		select {
		case <-ctx.Done():
			result <- false
			return
		default:
		}

		if i.Cmp(&end) >= 0 {
			break
		}

		if mod.Mod(&n, &i).Cmp(zero) == 0 {
			result <- false
			cancel()
			return
		}
		i.Add(&i, &step)
	}
	result <- true
}
