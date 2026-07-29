# REF-P7-25-R2-B1A-C3E2 / Canonicalization-scope false-rejection review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E2-RESOLVED-EXECUTABLE-V1`

**Decision：**
`ACCEPTED_PRE_ROOT_FALSE_REJECTION_PARSE_PREDICATE_CROSSED_OWNER_BOUNDARY`

## 1. Evidence

```text
EXECUTION_RESULT.md §56 SHA-256 =
  7b8240ff9f1babd92c04d4817e2f96b9f08a5dcdcb401e06c78d3da09e8abb77
reviewed PLAN SHA-256 =
  50455df1dd1383a8ce37482042ea4d1ba99e7c1d35a86087060df4ee96ec3a80
reviewed FULL SHA-256 =
  e43c6bd62f4fc8ba65dd287b14d2e587cef76d4cfb6219a44d7182c20552bfd0
HEAD = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
staged paths = 0
C3E2 fixed container = absent
```

Resolved executable与`TestLoader` probe均pass。Controller strict parsed PLAN、CANDIDATE、FULL三行，但把candidate-specific
canonical-byte predicate用于所有rows，在FULL subset comparison与root creation前报`noncanonical machine JSON`。

## 2. Independent parse diagnosis

Planner独立重算：

```text
PLAN_MACHINE_CONTRACT strict parse = pass
PLAN_MACHINE_CONTRACT canonical sorted-key bytes = false
CANDIDATE_MACHINE_CONTRACT strict parse = pass
CANDIDATE_MACHINE_CONTRACT canonical sorted-key bytes = true
FULL_PLAN_MACHINE_STATE strict parse = pass
FULL_PLAN_MACHINE_STATE canonical sorted-key bytes = false
```

Reviewed PLAN §3只把canonical reserialization byte equality及exact payload SHA绑定到candidate。PLAN machine只需strict parse；
FULL machine只需strict parse并对nested required subset做exact comparison。Controller增加了未授权的跨owner predicate。

故这是execution-controller false rejection，不是runtime、FULL subset、candidate、implementation或science failure。Root/clone/
source/tests/commit/manifest/R3 reads和所有device/network/formal副作用均0。

## 3. Successor ownership contract

Fresh successor必须在`PLAN_MACHINE_CONTRACT`内建立唯一`machine_row_parse_policy` mapping：

- PLAN row：duplicate-key/non-finite rejecting strict parse only；不要求canonical bytes或payload SHA；
- FULL row：同样strict only；parse后另做required FULL exact subset；
- CANDIDATE row：strict parse + canonical exact bytes + PLAN-machine-bound exact-byte SHA。

Controller只能按mapping中对应row policy执行；禁止共享、继承、union或跨owner扩展predicate。其余nested FULL merge、唯一candidate
object、resolved executable probe、fresh root、source evidence-before-compare、clean-room unittest各一次、candidate edit0、single
commit/manifest、original R3 three-hash、retry0及zero side-effect合同不变。无Advisor/Human gate。

建议FULL将C3E2记录为accepted false rejection，并按successor nested required state程序化激活successor；candidate SHA、checkpoint、
release与R3状态不变。

