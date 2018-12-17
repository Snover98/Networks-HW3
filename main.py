import numpy as np
import sys
from collections import deque


def parse_input(inp):
    # seperate input by spaces (assumes input is a string)
    seperated = inp

    # calculate T,M,N
    T = int(seperated[0])
    N = int(seperated[1])
    M = int(seperated[2])

    # input size should be that
    assert (len(seperated) == 3 + M * N + N + 2 * M)

    # var for the next unread input
    next_unread = 3

    # create a list of all probabilities
    P = np.reshape(np.asarray(seperated[next_unread:next_unread + M * N], np.float64), (N, M))
    # update next_unread
    next_unread += M * N

    # occurance rates
    L = np.asarray(seperated[next_unread:next_unread + N], np.float64)
    # update next_unread
    next_unread += N

    # sizes of queues
    Q = np.asarray(seperated[next_unread:next_unread + M], np.int32)
    # update next_unread
    next_unread += M

    # broadcast rates
    V = np.asarray(seperated[next_unread:next_unread + M], np.float64)
    # update next_unread
    next_unread += M

    # next unread should be the size of the input
    assert (next_unread == len(seperated))

    # return the values
    return T, N, M, P, L, Q, V

def main():
    # parse input
    T, N, M, P, L, Q, V = parse_input(sys.argv[1:])

    # broadcast queues for ports
    queues = [deque() for _ in Q]

    Y = np.zeros(shape=M)
    X = np.zeros(shape=M)

    total_wait_time = 0.0
    total_service_time = 0.0

    cur_time = 0

    while cur_time < T or sum([len(q) for q in queues]) > 0:
        # print("TIME IS {t}".format(t=cur_time))
        occurances = [np.random.poisson(l) for l in L]

        broadcasts = [np.random.poisson(v) for v in V]



        # print(occurances)
        # print(broadcasts)

        # incoming packets
        if(cur_time < T):
            for idx, packets in enumerate(occurances):
                for _ in range(packets):
                    out_port = np.random.choice(range(M), p=P[idx])
                    queues[out_port].append(cur_time)

        # for port in range(M):
        #     print(len(queues[port]))
        #     print(queues[port])

        for port, num_broadcasted in enumerate(broadcasts):
            # print(num_broadcasted)
            # print(len())
            for _ in range(num_broadcasted):
                if not len(queues[port]) == 0:
                    # broadcast first pack in queue and add to total time
                    broadcasted_pack = queues[port].popleft()
                    total_service_time += cur_time - broadcasted_pack
                    # print("BROADCASTED PACK AT TIME {t}".format(t=cur_time))
                    Y[port] += 1

                if not len(queues[port]) == 0:
                    # update total time for pack that is now getting service
                    service_package = queues[port].popleft()
                    total_wait_time += cur_time - service_package
                    queues[port].appendleft(service_package)

            while len(queues[port]) > Q[port]:
                queues[port].pop()
                X[port] += 1

            assert (len(queues[port]) <= Q[port])

        # for port in range(M):
            # print(queues[port])
            # assert(len(queues[port]) <= Q[port])

        # print(queues)
        cur_time += 1

    # print(total_wait_time, total_service_time)

    T_w = total_wait_time / float(sum(Y))
    T_s = total_service_time / float(sum(Y))

    str_Y = str(sum(Y)) + " "
    str_X = str(sum(X)) + " "
    for i in range(len(Y)):
        str_Y += str(Y[i]) + " "
        str_X += str(X[i]) + " "

    print(str_Y + str_X + "{tot_T} {T_w} {T_s}".format(tot_T=cur_time, T_w=T_w, T_s=T_s))


if __name__ == '__main__':
    main()