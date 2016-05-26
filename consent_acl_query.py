
SQL = """
select e.*
 from ACL_ENTRY e, ACL_OBJECT_IDENTITY i, ACL_SID a, ACL_CLASS c
 where e.ACL_OBJECT_IDENTITY = i.ID
 and i.OWNER_SID = a.ID
 and a.SID='rscl1002'
 and i.OBJECT_ID_IDENTITY=4002
 and i.OBJECT_ID_CLASS=c.ID
 and c.class like '%ConsentHeader'
 """;

