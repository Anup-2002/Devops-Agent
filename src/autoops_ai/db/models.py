from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Boolean, DateTime, Enum as SQLEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from autoops_ai.db.base import Base, TimestampMixin


class UserRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class DeploymentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class Team(Base, TimestampMixin):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    __table_args__ = (UniqueConstraint("organization_id", "name", name="uq_team_org_name"),)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False, default=UserRole.MEMBER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class TeamMembership(Base, TimestampMixin):
    __tablename__ = "team_memberships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("team_id", "user_id", name="uq_team_membership"),)


class Agent(Base, TimestampMixin):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    configuration: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class Deployment(Base, TimestampMixin):
    __tablename__ = "deployments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    environment: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[DeploymentStatus] = mapped_column(SQLEnum(DeploymentStatus), nullable=False, default=DeploymentStatus.PENDING)


class DeploymentRun(Base, TimestampMixin):
    __tablename__ = "deployment_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deployment_id: Mapped[int] = mapped_column(ForeignKey("deployments.id", ondelete="CASCADE"), nullable=False)
    triggered_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[DeploymentStatus] = mapped_column(SQLEnum(DeploymentStatus), nullable=False, default=DeploymentStatus.PENDING)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class DeploymentHistory(Base):
    __tablename__ = "deployment_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deployment_run_id: Mapped[int] = mapped_column(ForeignKey("deployment_runs.id", ondelete="CASCADE"), nullable=False)
    previous_status: Mapped[DeploymentStatus] = mapped_column(SQLEnum(DeploymentStatus), nullable=False)
    new_status: Mapped[DeploymentStatus] = mapped_column(SQLEnum(DeploymentStatus), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Incident(Base, TimestampMixin):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    deployment_id: Mapped[int] = mapped_column(ForeignKey("deployments.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[IncidentSeverity] = mapped_column(SQLEnum(IncidentSeverity), nullable=False)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class IncidentLog(Base, TimestampMixin):
    __tablename__ = "incident_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)


class RCAReport(Base, TimestampMixin):
    __tablename__ = "rca_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, unique=True)
    root_cause: Mapped[str] = mapped_column(Text, nullable=False)
    impact_assessment: Mapped[str] = mapped_column(Text, nullable=False)
    timeline: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class MonitoringMetric(Base, TimestampMixin):
    __tablename__ = "monitoring_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deployment_id: Mapped[int] = mapped_column(ForeignKey("deployments.id", ondelete="SET NULL"), nullable=True)
    metric_name: Mapped[str] = mapped_column(String(128), nullable=False)
    metric_value: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False)
    labels: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    monitoring_metric_id: Mapped[int] = mapped_column(ForeignKey("monitoring_metrics.id", ondelete="CASCADE"), nullable=False)
    deployment_id: Mapped[int] = mapped_column(ForeignKey("deployments.id", ondelete="SET NULL"), nullable=True)
    threshold: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False)
    current_value: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class GitCommit(Base, TimestampMixin):
    __tablename__ = "git_commits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deployment_run_id: Mapped[int] = mapped_column(ForeignKey("deployment_runs.id", ondelete="SET NULL"), nullable=True)
    commit_sha: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    author_email: Mapped[str] = mapped_column(String(320), nullable=False)


class PullRequest(Base, TimestampMixin):
    __tablename__ = "pull_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    git_commit_id: Mapped[int] = mapped_column(ForeignKey("git_commits.id", ondelete="SET NULL"), nullable=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(64), nullable=False)


class TestResult(Base, TimestampMixin):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deployment_run_id: Mapped[int] = mapped_column(ForeignKey("deployment_runs.id", ondelete="CASCADE"), nullable=False)
    suite_name: Mapped[str] = mapped_column(String(255), nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    total_tests: Mapped[int] = mapped_column(Integer, nullable=False)
    failed_tests: Mapped[int] = mapped_column(Integer, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(128), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(128), nullable=False)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


Organization.teams = relationship(Team, backref="organization", cascade="all, delete-orphan")
Organization.users = relationship(User, backref="organization", cascade="all, delete-orphan")
Team.memberships = relationship(TeamMembership, backref="team", cascade="all, delete-orphan")
User.memberships = relationship(TeamMembership, backref="user", cascade="all, delete-orphan")
Team.agents = relationship(Agent, backref="team", cascade="all, delete-orphan")
Deployment.runs = relationship(DeploymentRun, backref="deployment", cascade="all, delete-orphan")
DeploymentRun.history = relationship(DeploymentHistory, backref="deployment_run", cascade="all, delete-orphan")
Incident.logs = relationship(IncidentLog, backref="incident", cascade="all, delete-orphan")
Incident.rca_report = relationship(RCAReport, backref="incident", uselist=False, cascade="all, delete-orphan")
