from complexityestimator.codereader import CodeReader
from complexityestimator.complexityestimator import ComplexityEstimator
from complexityestimator.args_parser import parser


def main():
    args = parser.parse_args()

    main_code_reader = CodeReader("_N_")
    main_code_reader.read_from_file(args.main)
    main_f = main_code_reader.get_function()

    init_f = lambda x: None
    if args.initialize != None:
        init_code_reader = CodeReader("_N_")
        init_code_reader.read_from_file(args.main)
        init_f = main_code_reader.get_function()

    clean_f = lambda x: None
    if args.clean != None:
        clean_code_reader = CodeReader("_N_")
        clean_code_reader.read_from_file(args.main)
        clean_f = main_code_reader.get_function()

    estimator = ComplexityEstimator(init_f, main_f, clean_f, args.timeout)
    data = estimator.estimate_complexity()

    print("Szacowana złożoność: %s" % data[0])
