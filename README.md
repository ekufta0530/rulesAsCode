**WIP** 

### Requirements:
- Update rules via pull requests/ code workflow
- Have repository of rules accessible in github with all Pro, Private, OSS and Community rules as desired
- Pull upstream changes to rules when Semgrep makes changes 
- Be able to publish rules to semgrep registry so `semgrep ci` will work when run. Eliminate clobbering on Semgrep private registry.

### Context: 

The big issue we are solving is the clobbering of the rules when a rule is uploaded via `semgrep publish`. In the Semgrep backend, rules are stored in a database with a rule identifier. This is something like `go.lang.security.injection.open-redirect.open-redirect` . This exact syntax is represented in the (Semgrep Registry)[https://semgrep.dev/r?q=go.lang.security.injection.open-redirect.open-redirect] but is not apparent in the rule editor where it looks like a simple folder structure. This is just a design from UX to make it easy to find the rules you are looking to edit.

As opposed to the rule registry, the (Semgrep Community Rules repo)[https://github.com/semgrep/semgrep-rules] and our Private Pro Rules Repo are actually in a familiar directory structured format living in a github repo. For example, the go.lang.security.injection.open-redirect.open-redirect rule is living in (go/lang/security/injection/open-redirect.yaml)[https://github.com/semgrep/semgrep-rules/blob/develop/go/lang/security/injection/open-redirect.yaml]. Notice that there is an extra ".open-redirect" in the dot format: go.lang.security.injection.open-redirect.**open-redirect**. This is because the `id` in the yaml of the rule is appended to the rule identifier.

Now the question is, how does Semgrep internally go from this directory structure to the dot format when our security analaysts are updating rules every hour? It is just a cron job that packages up the files in the repo in the dot format and publishes them to our database. The solution we are working on in this project is really just a public version of what we are doing internally!

Why do we need to do this if Semgrep already is? Well, the difference is that `semgrep publish` doesn't do what our private internal script does with packaging the familiar directory structure into the dot format we use in the backend. The behavior of `semgrep publish` is to send the rule to the registry and save it as `your_org_slug.id_from_the_rule_yaml`. Example below:

```yaml
rules:
  - id: open-redirect
    languages: [ go ]
    severity: WARNING
    message: ...
```

For an org with the slug "acme_corp", publishing this rule will save it in the registry as acme_corp.open-redirect. It doesn't matter the path of where the file came from. If there are more rules with `id: open-redirect` then they will clobber each other/ overwrite the previous one resulting in only the last one uploaded to persist.


## Steps to make this work:
WIP

### Getting the rules in our repo

(1a) Manually add the rules we want via the (Registry)[https://semgrep.dev/explore]. This should just be necessary for the initial setup. 

(1b) Pull all rules from the special /all endpoint. This endpoint has all of the rules in our org defined by the SEMGREP_APP_TOKEN we are using.

```bash
curl --location 'https://semgrep.dev/c/r/all' \
--header 'Authorization: Bearer $SEMGREP_APP_TOKEN'
```

(1c) Parse them and save files with semgrep registry dot syntax. Now we have a large list of files in one folder.
This work is being done in (ruleParser.py)[https://github.com/ekufta0530/rulesAsCode/blob/main/ruleParser.py]

Optional: recreate directory structure from dot syntax go.security.sql-injection.sqlinjection.yaml becomes go/security/sql-injection (note: the ruleid in the yaml is appended to rule identifier in the registry). This potentially allows for easier navigation in the github repo. 

(1d) `semgrep publish` will now send those rules to the registry without clobbering each other. This is because the full path is represented as the id in the rule yaml file. For example, the open-redirect community rule we referenced above looks different after the parser is done with it:

```yaml
rules:
- id: go.lang.security.injection.open-redirect.open-redirect
  languages:
  - go
  severity: WARNING
  message: ...
```

This should meet the requirements for being able to make changes to the rules via PRs and `semgrep publish` them via a workflow. Now, on to solving the issue of getting upstream updates when semgrep security researchers make changes.

### Pulling upstream changes made by Semgrep

(2a) How can we get upstream? Two possible options:
- Directly from private & public rule repos
- curling a /all endpoint for specific rulesets (Check if this exists)

(2b) Create a new branch with these 
Next, the 
Likely solution is to create a new branch from these upstream rules and then compare changes to merge. 

## Limitations

Assigning policies easily to rules. The policies API is a focus for the semgrep team q2 2024. This will offer the best solution. Solution in meantime may be to output accessible links for any new rules. 