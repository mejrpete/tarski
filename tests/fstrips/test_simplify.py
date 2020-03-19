from tarski.benchmarks.counters import generate_fstrips_counters_problem
from tarski.fstrips import UniversalEffect
from tarski.fstrips.manipulation.simplify import Simplify
from tarski.syntax import symref, land, lor, neg, bot, top, forall
from tests.common import blocksworld


def test_replacement_of_static_terms_by_constants():
    problem = generate_fstrips_counters_problem(ncounters=3)
    lang = problem.language
    value, max_int, counter, val_t, c1 = lang.get('value', 'max_int', 'counter', 'val', 'c1')
    x = lang.variable('x', counter)
    two, three, six = [lang.constant(c, val_t) for c in (2, 3, 6)]

    s = Simplify(problem, problem.init)
    assert symref(s.simplify_expression(x)) == symref(x)
    assert symref(s.simplify_expression(value(c1) < max_int())) == symref(value(c1) < six)  # max_int evaluates to 6
    assert s.simplify_expression(two < max_int()) is True
    assert s.simplify_expression(two > three) is False

    # conjunction evaluates to false because of first conjunct:
    falseconj = land(two > three, value(c1) < max_int())
    assert s.simplify_expression(falseconj) is False
    assert s.simplify_expression(neg(falseconj)) is True

    # first conjunct gets removed:
    assert str(s.simplify_expression(land(two < three, value(c1) < max_int()))) == '<(value(c1),6)'

    # first disjunct gets removed because it is false
    assert str(s.simplify_expression(lor(two > three, value(c1) < max_int()))) == '<(value(c1),6)'

    assert str(s.simplify_expression(forall(x, value(x) < max_int()))) == 'forall x : (<(value(x),6))'
    assert s.simplify_expression(forall(x, two + three <= 6)) is True

    inc = problem.get_action('increment')
    simp = s.simplify_action(inc)
    assert str(simp.precondition) == '<(value(c),6)'
    assert str(simp.effects) == str(inc.effects)

    eff = UniversalEffect(x, [value(x) << three])
    assert str(s.simplify_effect(eff)) == '(T -> forall (x) : ((T -> value(x) := 3)))'

    simp = s.simplify()
    assert str(simp.get_action('increment').precondition) == '<(value(c),6)'


def test_simplification_of_negation():
    problem = blocksworld.generate_small_strips_bw_problem()
    lang = problem.language
    b1, clear, on, ontable, handempty, holding = lang.get('b1', 'clear', 'on', 'ontable', 'handempty', 'holding')

    s = Simplify(problem, problem.init)
    cb1 = clear(b1)
    assert str(s.simplify_expression(land(cb1, neg(bot)))) == 'clear(b1)'
    assert str(s.simplify_expression(cb1)) == 'clear(b1)'  # No evaluation made
    assert str(s.simplify_expression(neg(neg(cb1)))) == 'clear(b1)'  # Double negation gets removed

    assert s.simplify_expression(land(neg(bot), neg(bot))) is True
    assert s.simplify_expression(lor(neg(top), neg(bot))) is True
    assert s.simplify_expression(lor(neg(top), neg(top))) is False

    act = problem.get_action('unstack')
    simp = s.simplify_action(act)
    assert simp