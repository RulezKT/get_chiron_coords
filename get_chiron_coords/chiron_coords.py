import array

from pydantic import BaseModel


class FileRecords(BaseModel):
    rec_start_addr: int
    int_len: float
    rsize: float


CHIRON_FILE_RECORDS: tuple[FileRecords] = (
    {
        # SUN
        "rec_start_addr": 0,
        "seg_start_time": 0,
        "seg_last_time": 0,
        "int_len": 0,
        "rec_last_addr": 0,
        # "rsize": 0,
    },
    {
        # 1
        "rec_start_addr": 8_065,
        "seg_start_time": -120_450_514.89409208,
        "seg_last_time": 510_321_600,
        "int_len": 510_321_600,
        "rec_last_addr": 54_071,
        # "rsize": 20,
        # init =  391_827_779.23949105
        # n =  500.0
    },
    {
        # 2
        "rec_start_addr": 54_072,
        "seg_start_time": -780_357_478,
        "seg_last_time": -120_450_514,
        "int_len": -120_450_514,
        "rec_last_addr": 100_078,
        # "rsize": 20,
        # init =  -256344669.7390517
        # n =  500.0
    },
    {
        # 3
        "rec_start_addr": 100_079,
        "seg_start_time": -1_428_684_898,
        "seg_last_time": -780_357_478,
        "int_len": -780_357_478,
        "rec_last_addr": 146_085,
        # "rsize": 20,
        # init =  -909271241.4267497
        # n =  500.0
    },
    {
        # 4
        "rec_start_addr": 146_086,
        "seg_start_time": -2_072_145_540,
        "seg_last_time": -1_428_684_898,
        "int_len": -1_428_684_898,
        "rec_last_addr": 192_092,
        # "rsize": 20,
        # init =  -1559481315.7158456
        # n =  500.0
    },
    {
        # 5
        "rec_start_addr": 192_093,
        "seg_start_time": -2_719_741_734,
        "seg_last_time": -2_072_145_540,
        "int_len": -2_072_145_540,
        "rec_last_addr": 238_099,
        # "rsize": 20,
        # init =  -2202930574.1405
        # n =  500.0
    },
    {
        # 6
        "rec_start_addr": 238_100,
        "seg_start_time": -3_155_716_800,
        "seg_last_time": -2_719_741_734,
        "int_len": -2_758_703_306,
        # intlen =  -2758703306.856402 ??????????????
        "rec_last_addr": 268_464,
        # "rsize": 20,
        # init =  -2891244118.0133157
        # n =  330.0
    },
    {
        # 7
        "rec_start_addr": 268_465,
        "seg_start_time": 510_321_600,
        "seg_last_time": 1_134_172_990,
        "int_len": 1_134_172_990,
        "rec_last_addr": 314_471,
        # "rsize": 20,
        # init =  1002901396.5747848
        # n =  500.0
    },
    {
        # 8
        "rec_start_addr": 314_472,
        "seg_start_time": 1_134_172_990,
        "seg_last_time": 1_785_159_000,
        "int_len": 1_785_159_000,
        "rec_last_addr": 360_478,
        # "rsize": 20,
        # init =  1655649864.227839
        # n =  500.0
    },
    {
        # 9
        "rec_start_addr": 360_479,
        "seg_start_time": 1_785_159_000,
        "seg_last_time": 2_451_382_230,
        "int_len": 2_451_382_230,
        "rec_last_addr": 406_485,
        # "rsize": 20,
        # init =  2313659513.647009
        # n =  500.0
    },
    {
        # 10
        "rec_start_addr": 406_486,
        "seg_start_time": 2_451_382_230,
        "seg_last_time": 3_098_798_447,
        "int_len": 3_098_798_447,
        "rec_last_addr": 452_492,
        # "rsize": 20,
        # init =  2967630632.730112
        # n =  500.0
    },
    {
        # 11
        "rec_start_addr": 452_493,
        "seg_start_time": 3_098_798_447,
        "seg_last_time": 3_187_252_800,
        "int_len": 3_187_252_800,
        "rec_last_addr": 458_842,
        # "rsize": 20,
        # init =  3185947430.156654
        # n =  69.0
    },
)


def LSTLTD(X: float, ARRAY: tuple[int]) -> int:
    # Find the index of the largest array element less than a given number X in an array of non-decreasing numbers.
    # The function returns the index of the last element of ARRAY that  is less than X.
    # DOUBLE PRECISION   ARRAY ( * )  is an array of double precision numbers that forms a  non-decreasing sequence. The elements of array need not  be distinct.

    length = len(ARRAY)
    if length == 0:
        return -1
    if X < ARRAY[0]:
        return 0
    if X > ARRAY[-1]:
        return length - 1

    BEGIN = 0
    END = length - 1

    # X lies between some pair of elements of the array
    while length > 2:
        # print("Items = ", N)
        MIDDLE = int(length / 2)

        if ARRAY[BEGIN + MIDDLE] < X:
            BEGIN += MIDDLE
        else:
            END -= MIDDLE

        length = END - BEGIN + 1

    return BEGIN


def chiron_coords(dateInSeconds, chiron_file: bytes):
    total_summaries_number = 10

    arrayInfoOffset = 0
    # internalOffset = 0

    arrayInfo = {
        "init": 0.0,  # start time of the first record in array
        "intlen": 0.0,  # the length of one record (seconds)
        # "rsize": 0.0,  # number of elements in one record
        "maxdim": 0.0,  # Maximum dimension
        # Double precision numbers stored in each MDA record
        # recsize = max(71, 4*maxdim + 11)
        "n": 0.0,  # number of records in segment
    }

    for i_summ in range(1, total_summaries_number + 1):
        if (
            CHIRON_FILE_RECORDS[i_summ]["seg_start_time"] < dateInSeconds
            and CHIRON_FILE_RECORDS[i_summ]["seg_last_time"] > dateInSeconds
        ):
            # print("number of segment =", i_summ)
            # console.log(`from  for in get_coordinates`);
            # console.log(`${this.file_header.summaries_line_struct[i].target_code}`);

            #   /*
            #         console.log(`from calc_geocentric_equ_cartes_pos x = ${coordinates_of_object.x} y = ${coordinates_of_object.y} z = ${coordinates_of_object.z}`);

            #         printf("get_coordinates Found: [%d] = ", i);
            #         printf(" %f,", file_header_ptr->summaries_line_struct[i].segment_start_time); # в сек от J2000
            #         printf(" %f,", file_header_ptr->summaries_line_struct[i].segment_last_time); # в сек от J2000
            #         printf(" %s[%d] , ", planet_name(file_header_ptr->summaries_line_struct[i].target_code), i);
            #         printf(" %s[%d], ", planet_name(file_header_ptr->summaries_line_struct[i].center_code), i);
            #         printf(" %d, ", file_header_ptr->summaries_line_struct[i].record_start_adress);
            #         printf(" %d, ", file_header_ptr->summaries_line_struct[i].record_last_adress);
            #         printf("\n");
            #         */

            #   /*
            #         The records within a segment are ordered by increasing initial epoch. All records contain the same number
            #         of coefficients. A segment of this type is structured as follows:

            #         +---------------+
            #         | Record 1      |
            #         +---------------+
            #         | Record 2      |
            #         +---------------+
            #     .
            #     .
            #     .
            #         +---------------+
            #         | Record N      |
            #         +---------------+
            #         | INIT          |
            #         +---------------+
            #         | INTLEN        |
            #         +---------------+
            #         | RSIZE         |
            #         +---------------+
            #         | N             |
            #         +---------------+
            #         */

            #   /* встаем на позицию 4 слова до конца summaries_line_struct[i]
            arrayInfoOffset = (CHIRON_FILE_RECORDS[i_summ]["rec_last_addr"] - 4) * 8
            # console.log(`${array_info_offset}`);

            #   /* читаем
            #         double init - start time of the first record in array
            #         double intlen - the length of one record (seconds)
            #         double rsize - number of elements in one record
            #         double n - number of records in segment */
            arrayInfo = array.array(
                "d", chiron_file[arrayInfoOffset : arrayInfoOffset + 32]
            )
            # init = arrayInfo[0]
            # print("init = ", init)
            # intlen = arrayInfo[1]
            # print("intlen = ", intlen)
            max_dim = int(arrayInfo[2])
            # print("max_dim = ", max_dim)
            if max_dim > 25:
                print("max_dim is greater than 25 !!!")
            # rsize = (4 * max_dim) + 11
            DFLSIZ = (4 * max_dim) + 11
            MAXDIM = max_dim
            #             !     MAXTRM      is the maximum number of terms allowed in each
            # !                 component of the difference table contained in a type
            # !                 21 SPK difference line. MAXTRM replaces the fixed
            # !                 table parameter value of 15 used in SPK type 1
            # !                 segments.
            # !                 Type 21 segments have variable size. Let MAXDIM be
            # !                 the dimension of each component of the difference
            # !                 table within each difference line. Then the size
            # !                 DLSIZE of the difference line is
            # !
            # !                    ( 4 * MAXDIM ) + 11
            # !
            # !                 MAXTRM is the largest allowed value of MAXDIM.
            # !
            # !
            #    INTEGER               MAXTRM
            #    PARAMETER           ( MAXTRM = 25 )
            # print("rsize = ", rsize)
            n_of_rec = int(arrayInfo[3])
            # print("n = ", n)

            # Number of directory epochs
            BUFSIZ = 100
            n_of_dir = n_of_rec // BUFSIZ
            # print("ndir = ", ndir)

            start_adress = CHIRON_FILE_RECORDS[i_summ]["rec_start_addr"]
            last_adress = CHIRON_FILE_RECORDS[i_summ]["rec_last_addr"]
            OFFD = last_adress - n_of_dir - 2
            OFFE = OFFD - n_of_rec

            final_record = []
            if n_of_rec <= BUFSIZ:
                print("number of records <= 100")
                data = array.array(
                    "d", chiron_file[(OFFE + 1) * 8 : (OFFE + n_of_rec) * 8 + 8]
                )[0]
                RECNO = LSTLTD(dateInSeconds, data)
                OFFR = start_adress - 1 + (RECNO + 1) * DFLSIZ
                final_record = array.array(
                    "d", chiron_file[(OFFR) * 8 : (OFFR + DFLSIZ) * 8]
                )

            else:
                for dir in range(0, n_of_dir):
                    data = array.array(
                        "d", chiron_file[(OFFD + dir) * 8 : (OFFD + dir) * 8 + 8]
                    )[0]
                    if data > dateInSeconds:
                        OFFD = OFFE + (dir) * BUFSIZ
                        data = array.array(
                            "d", chiron_file[(OFFD) * 8 : (OFFD + BUFSIZ) * 8]
                        ).tolist()
                        index_of_rec = LSTLTD(dateInSeconds, data)
                        RECNO = dir * BUFSIZ + index_of_rec

                        OFFR = start_adress - 1 + (RECNO + 1) * DFLSIZ
                        final_record = array.array(
                            "d", chiron_file[(OFFR) * 8 : (OFFR + DFLSIZ) * 8]
                        )
                        break
                if not final_record:
                    print("chiron final records sec = ", dateInSeconds)
                    Ind = n_of_rec % BUFSIZ
                    data = array.array(
                        "d",
                        chiron_file[
                            (last_adress - n_of_dir - Ind - 1) * 8 : (
                                last_adress - n_of_dir - 2
                            )
                            * 8
                        ],
                    )
                    RECNO = (n_of_dir) * BUFSIZ + LSTLTD(dateInSeconds, data)
                    OFFR = start_adress - 1 + (RECNO + 1) * DFLSIZ
                    final_record = array.array(
                        "d", chiron_file[(OFFR) * 8 : (OFFR + DFLSIZ) * 8]
                    )

            mda_record = final_record

            # initialize arrays for spke01
            # self.G = zeros(15)
            # self.REFPOS = zeros(3)
            # self.REFVEL = zeros(3)
            # self.KQ = array([0, 0, 0])
            # self.FC = zeros(15)
            # self.FC[0] = 1.0
            # self.WC = zeros(13)
            # self.W = zeros(17)

            #     print(mda_record)

            # max_dim_temp = int(mda_record[0])
            # print("max_dim_temp = ", max_dim_temp)

            # MAXTRM = 25
            TL = mda_record[0]
            # print("TL = ", TL)
            G = mda_record[1 : max_dim + 1].tolist()
            # print(id(REFPOS[0]))
            # print(id(mda_record[max_dim + 1]))
            # print("G = ", G)
            # print(G)
            #
            #     Collect the reference position and velocity.
            #
            REFPOS = [
                mda_record[max_dim + 1],
                mda_record[max_dim + 3],
                mda_record[max_dim + 5],
            ]

            REFVEL = [
                mda_record[max_dim + 2],
                mda_record[max_dim + 4],
                mda_record[max_dim + 6],
            ]

            # print("REFPOS[0] = ", REFPOS[0])

            KQMAX1 = int(mda_record[4 * max_dim + 7])
            KS = KQMAX1 - 1
            # print("KQMAX1 = ", KQMAX1)
            KQ = [
                int(mda_record[4 * max_dim + 8]),
                int(mda_record[4 * max_dim + 9]),
                int(mda_record[4 * max_dim + 10]),
            ]
            # print("KQ = ", KQ)

            MQ2 = KQMAX1 - 2
            DELTA = dateInSeconds - TL
            TP = DELTA

            #     This is clearly collecting some kind of coefficients.
            #     The problem is that we have no idea what they are...
            #
            #     The G coefficients are supposed to be some kind of step size
            #     vector.
            #
            #     TP starts out as the delta t between the request time
            #     and the time for which we last had a state in the MDL file.
            #     We then change it from DELTA  by the components of the stepsize
            #     vector G.
            #

            FC = [0 for i in range(max_dim)]
            FC[0] = 1.0
            WC = [0 for i in range(max_dim - 1)]
            # print("FC :")
            # print(FC)
            # print("WC :")
            # print(WC)

            # for J in range(1, MQ2 + 1):
            #     FC[J] = TP / G[J - 1]
            #     WC[J - 1] = DELTA / G[J - 1]
            #     TP = DELTA + G[J - 1]

            for J in range(1, MQ2 + 1):
                if G[J - 1] == 0.0:
                    print(
                        "SPKE21\nA value of zero was found at index {0} "
                        + "of the step size vector."
                    )
                FC[J] = TP / G[J - 1]
                WC[J - 1] = DELTA / G[J - 1]
                TP = DELTA + G[J - 1]

            W = [0 for i in range(max_dim + 2)]
            #
            #     Collect KQMAX1 reciprocals.
            #     KS = KQMAX1 - 1     KS = KQMAX1 - 1
            # for J in range(1, KQMAX1 + 1):
            #     W[J - 1] = 1.0 / float(J)
            for J in range(1, KQMAX1 + 1):
                W[J - 1] = 1.0 / float(J)
            #
            #     Compute the W(K) terms needed for the position interpolation
            #     (Note,  it is assumed throughout this routine that KS, which
            #     starts out as KQMAX1-1 (the ``maximum integration'')
            #     is at least 2.
            #

            # print("KS from start = ", KS)

            JX = 0
            KS1 = KS - 1

            while KS >= 2:
                JX = JX + 1

                for J in range(1, JX + 1):
                    W[J + KS - 1] = FC[J] * W[J + KS1 - 1] - WC[J - 1] * W[J + KS - 1]

                KS = KS1
                KS1 = KS1 - 1

            #
            #     Perform position interpolation: (Note that KS = 1 right now.
            #     We don't know much more than that.)
            #

            STATE = [0, 0, 0]

            # print("KS = ", KS)

            # print("KQ= ", KQ)

            # print(DTtest[9])

            # DTtest = reshape(
            #     mda_record[MAXDIM + 7 : MAXDIM * 4 + 7], (MAXDIM, 3), order="F"
            # )

            # print(DTtest)

            DTtest = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]

            start = max_dim + 7
            for i in range(max_dim):
                DTtest[i][0] = mda_record[start + i]
            for i in range(max_dim):
                DTtest[i][1] = mda_record[start + max_dim + i]

            for i in range(max_dim):
                DTtest[i][2] = mda_record[start + max_dim * 2 + i]

            # print(DTtest)

            # start = max_dim + 7
            # columns = 3
            # DTtest = [
            #     [
            #         mda_record[start + j * columns + i : start + j * columns + 1 + i][0]
            #         for i in range(columns)
            #     ]
            #     for j in range(max_dim)
            # ]

            for Ii in range(3):
                KQQ = KQ[Ii]
                SUM = 0.0

                for J in range(KQQ, 0, -1):
                    # v SUM = SUM + DTtest[J - 1][Ii] * W[J - 1 + KS]
                    SUM = SUM + DTtest[J - 1][Ii] * W[J - 1 + KS]

                STATE[Ii] = REFPOS[Ii] + DELTA * (REFVEL[Ii] + DELTA * SUM)

            # print("KS = ", KS)
            # print("KS1 = ", KS1)

            return {
                "x": STATE[0],
                "y": STATE[1],
                "z": STATE[2],
            }

    return {
        "x": 0,
        "y": 0,
        "z": 0,
    }
