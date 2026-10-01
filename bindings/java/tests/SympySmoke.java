import apebind.generated.sympy_ape.SympyAPEBinding;

public class SympySmoke {
    public static void main(String[] args) {
        String version = String.valueOf(SympyAPEBinding.version());
        require(version.equals("1.14.0"), version);

        String integrated = String.valueOf(SympyAPEBinding.integrate(
            SympyAPEBinding.IntegrateParameters.builder()
                .expr("sin(x)")
                .build()));
        require(integrated.contains("result=-cos(x)"), integrated);

        String differentiated = String.valueOf(SympyAPEBinding.diff(
            SympyAPEBinding.DiffParameters.builder()
                .expr("-x**2")
                .build()));
        require(differentiated.contains("result=-2*x"), differentiated);

        String substituted = String.valueOf(SympyAPEBinding.subs(
            SympyAPEBinding.SubsParameters.builder()
                .expr("x**2+y")
                .symbols("x")
                .value("3")
                .build()));
        require(substituted.contains("result=y + 9"), substituted);
    }

    private static void require(boolean condition, String actual) {
        if (!condition) {
            throw new AssertionError(actual);
        }
    }
}
